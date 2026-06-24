from flask import Flask,jsonify,request, Blueprint
from ..services.servicios_extra import crear_servicio_extra, eliminar_servicio_extra, formato_mensaje_get, listar_servicios_extra, modificar_servicio_extra
from ..validators.servicios_extra import validar_body_patch_servicios_extra, validar_body_post_servicios_extra, validar_id_get_servicios_extra
from ..utils import requiere_auth

servicios_extra_bp = Blueprint('servicios_extra_bp', __name__)

@servicios_extra_bp.route('/servicios_extra', methods=['GET'])
def buscar_servicios_extra():

    id_servicio_extra_base = request.args.get('id') #me lo dan como string, lo convierto a integer 
    id_servicio_extra = None 
    nombre_servicio_extra = request.args.get('nombre_servicio')
   
#verificaciones sin conexion a db

    id_servicio_extra, error, codigo = validar_id_get_servicios_extra(id_servicio_extra_base)

    if error:
        return jsonify({"errors": [{"code": str(codigo), "message": "Parámetro erróneo", "level": "error", "description": error}]}), codigo

    if nombre_servicio_extra is not None and nombre_servicio_extra.strip() == "": #por si buscaron por servicio_extra pero no ingresaron nada
        return jsonify({"errors": [{"code": "400", "message": "Parámetro erróneo", "level": "error", "description": "El parámetro 'nombre_servicio' no puede estar vacío."}]}), 400
    
    try: 
        resultado = listar_servicios_extra(id_servicio_extra, nombre_servicio_extra)
        
        if (not resultado) and (id_servicio_extra or nombre_servicio_extra): 

            descripcion_error = []
            if nombre_servicio_extra:
                descripcion_error.append(f"nombre_servicio '{nombre_servicio_extra}'")
        
            if id_servicio_extra:
                descripcion_error.append(f"id '{id_servicio_extra}'")
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "servicio extra no encontrado",
                    "level": "error",
                    "description": f"No hay registros de servicios extra para: {', '.join(descripcion_error)}." #error personalizado segun que filtros se usaron
                }]
            }), 404


        return jsonify(resultado), 200 

    
    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500", 
                "message": "Error interno del servidor", 
                "level": "error", 
                "description": str(error_interno)
            }]
        }), 500

    

@servicios_extra_bp.route('/servicios_extra', methods=['POST'])
@requiere_auth(rol = 'admin')
def agregar_servicios_extra():

    datos = (request.json)
    error, codigo = validar_body_post_servicios_extra(datos)

    if error:
        return jsonify({
            "errors": [{
                "code": str(codigo),
                "message": "Datos inválidos para la creación de un servicio extra",
                "level": "error",
                "description": error
            }]
        }), codigo
    
    try:
        crear_servicio_extra(datos)
        return "",201

    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Error", "level": "error", "description": mensaje}]}), status

    except Exception as error_interno:
            return jsonify({
                "errors": [{
                    "code": "500",
                    "message": "Error interno del servidor",
                    "level": "error",
                    "description": str(error_interno)
                }]
            }), 500

@servicios_extra_bp.route('/servicios_extra/<int:id>', methods=['GET'])
def obtener_servicio_extra(id):
    try:
        resultado = listar_servicios_extra(id_servicio_extra=id, nombre_servicio_extra=None) #como quiero buscar por id, los otros filtros los dejo vacios para que no afecten la consulta
        if not resultado:
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "Servicio extra no encontrado",
                    "level": "error",
                    "description": f"No hay registros del servicios_extra para el id '{id}'."
                }]
            }), 404

        return jsonify(resultado[0]), 200 

    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500", 
                "message": "Error interno del servidor", 
                "level": "error", 
                "description": str(error_interno)
            }]
        }), 500


@servicios_extra_bp.route('/servicios_extra/<int:id>', methods=['PATCH'])
@requiere_auth(rol = 'admin')
def modificar_servicios_extra(id):
    
    conn = None
    cursor = None

    datos = request.get_json(silent=True) #si no se puede convertir a json, devuelve None 
    error, codigo = validar_body_patch_servicios_extra(datos)

    if error:
        return jsonify({
            "errors": [{
                "code": str(codigo), 
                "message": "Datos inválidos para la modificación de un servicio extra",
                "level": "error",
                "descripcion": error
            }]
        }), codigo

    try:
        modificar_servicio_extra(id,datos)
        return '', 204

    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Error", "level": "error", "description": mensaje}]}), status

    
    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": str(error_interno)
            }]
        }), 500
    
@servicios_extra_bp.route('/servicios_extra/<int:id>', methods=['DELETE'])
@requiere_auth(rol = 'admin')
def borrar_servicio_extra(id):

    if id == 0:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Parámetro erróneo o faltante",
                "level": "error",
                "description": "El id ingresado debe ser mayor estricto a 0"
            }]
        }), 400

    try:
        eliminar_servicio_extra(id)
        return "", 204
    

    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Error", "level": "error", "description": mensaje}]}), status

    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": str(error_interno)
            }]
        }), 500
    
