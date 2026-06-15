from flask import Flask,jsonify,request, Blueprint
from ..services.menu import formato_mensaje_get, listar_platos ,modificar_plato ,crear_plato, eliminar_plato
from ..validators.menu import validar_params_get_menu, validar_body_post_menu, validar_body_patch_menu
from ..utils import requiere_auth

menu_bp = Blueprint('menu_bp', __name__)


@menu_bp.route('/menu', methods=['GET'])
def buscar_platos_menu():

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    id_plato_base = request.args.get('id') #me lo dan como string, lo convierto a integer 
    id_plato = None 
    nombre_plato = request.args.get('plato')
    restricciones = request.args.getlist('restricciones_alimenticias') #para poder recibir en la request varias restricciones
                                                                       #recibo por ej: restricciones_alimenticias=sin_lactosa&restricciones_alimenticias=vegetariano
                                                                       #getlist entonces guarda en una lista ["sin_lactosa","vegetariano"]
#verificaciones sin conexion a db

    id_plato, error, codigo = validar_params_get_menu(id_plato_base, restricciones)

    if error:
        return jsonify({"errors": [{"code": str(codigo), "message": "Parámetro erróneo", "level": "error", "description": error}]}), codigo

    if nombre_plato is not None and nombre_plato.strip() == "": #por si buscaron por plato pero no ingresaron nada
        return jsonify({"errors": [{"code": "400", "message": "Parámetro erróneo", "level": "error", "description": "El parámetro 'plato' no puede estar vacío."}]}), 400
    
    try: 
        resultado = listar_platos(id_plato, nombre_plato, restricciones)
        
        if (not resultado) and (id_plato or nombre_plato or restricciones): 

            descripcion_error = []
            if nombre_plato:
                descripcion_error.append(f"plato '{nombre_plato}'")
            if restricciones:
                descripcion_error.append(f"restricciones '{','.join(restricciones)}'")
            if id_plato:
                descripcion_error.append(f"id '{id_plato}'")
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "Plato no encontrado",
                    "level": "error",
                    "description": f"No hay registros del menu para: {', '.join(descripcion_error)}." #error personalizado segun que filtros se usaron
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

#TODO: chequeo de rol admin
@menu_bp.route('/menu', methods=['POST'])
@requiere_auth()
def agregar_platos_menu():

    datos = (request.json)
    error, codigo = validar_body_post_menu(datos)

    if error:
        return jsonify({
            "errors": [{
                "code": str(codigo),
                "message": "Datos inválidos para la creación de un plato",
                "level": "error",
                "description": error
            }]
        }), codigo
    
    try:
        crear_plato(datos)
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


@menu_bp.route('/menu/<int:id>', methods=['GET'])
def obtener_plato_menu(id):
    try:
        resultado = listar_platos(id_plato=id, nombre_plato=None, restricciones=[]) #como quiero buscar por id, los otros filtros los dejo vacios para que no afecten la consulta
        if not resultado:
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "Plato no encontrado",
                    "level": "error",
                    "description": f"No hay registros del menu para el id '{id}'."
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


#TODO: chequeo de rol admin
@menu_bp.route('/menu/<int:id>', methods=['PATCH'])
@requiere_auth()
def modificar_platos_menu(id):

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    conn = None
    cursor = None

    datos = request.get_json(silent=True) #si no se puede convertir a json, devuelve None 
    error, codigo = validar_body_patch_menu(datos)

    if error:
        return jsonify({
            "errors": [{
                "code": str(codigo), 
                "message": "Datos inválidos para la modificación de un plato",
                "level": "error",
                "descripcion": error
            }]
        }), codigo

    try:
        modificar_plato(id,datos)
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

#TODO: chequeo admin
@menu_bp.route('/menu/<int:id>', methods=['DELETE'])
@requiere_auth()
def borrar_plato_menu(id):

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
        eliminar_plato(id)
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
    
