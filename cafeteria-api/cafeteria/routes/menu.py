
from flask import Flask,jsonify,request, Blueprint
from ..db import get_connection

menu_bp = Blueprint('menu_bp', __name__)

def validar_body_menu(cuerpo):

    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    plato = cuerpo.get("plato")
    precio = cuerpo.get("precio")
    descripcion = cuerpo.get("descripcion")
    restriccion = cuerpo.get("restricciones_alimenticias")
    
    if plato is None or precio is None or descripcion is None or restriccion is None:
        return "Faltan campos por asignar",400

    if (not isinstance(plato,str)) or (not isinstance(precio,int)) or (precio <= 0) or (not isinstance(descripcion,str)) or (not isinstance(restriccion,str)):
        return "El nombre del plato, su descripción y la restricción alimenticia (si abarca alguna) deben ser de tipo string. El precio debe ser de tipo integer y mayor a 0",400

    return None, None

@menu_bp.route('/menu', methods=['GET'])
def buscar_platos_menu():

    RESTRICCIONES = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten'] 

    id_plato = request.args.get('id', type=int) #me lo dan como string, lo convierto a integer 
    nombre_plato = request.args.get('plato')
    restriccion = request.args.get('restricciones_alimenticias')


#verificaciones sin conexion a db

    #ahora que id_plato es un integer
    if id_plato is not None and id_plato <= 0:
        return jsonify({
            "errors": [{
                "code": "400", 
                "message": "Parámetro erróneo", 
                "level": "error", 
                "description": "El id debe ser un entero positivo."
            }]
        }), 400


    if (restriccion) and (restriccion not in RESTRICCIONES):

        return jsonify({

            "errors": [{
                "code": "400",
                "message": "Parámetro erróneo",
                "level" : "error",
                "description": f"La restricción alimenticia '{restriccion}' no es válida para busqueda."
            }]
        }), 400


    query = "SELECT * FROM menu"
    filtros = []
    params = []

    if id_plato:
        filtros.append("id = %s")
        params.append(id_plato)

    if nombre_plato:
        filtros.append("plato LIKE %s")
        params.append(f"%{nombre_plato}%")      # %pizza% → contiene "pizza" sintaxis SQL

    if restriccion:
        filtros.append("restricciones_alimenticias = %s")
        params.append(restriccion)         

    if filtros:
        query += " WHERE " + " AND ".join(filtros) 


    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        resultado = cursor.fetchall()

        if (not resultado) and (id_plato or nombre_plato or restriccion): 

            descripcion = []
            if nombre_plato:
                descripcion.append(f"plato '{nombre_plato}'")
            if restriccion:
                descripcion.append(f"restricción '{restriccion}'")
            if id_plato:
                descripcion.append(f"id '{id_plato}'")

            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "Plato no encontrado",
                    "level": "error",
                    "description": f"No hay registros del menu para: {', '.join(descripcion)}." #error personalizado segun que filtros se usaron
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

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@menu_bp.route('/menu', methods=['POST'])
def agregar_platos_menu():
    
    conn = None
    cursor = None
    try:
        datos = request.json

        error, codigo = validar_body_menu(datos)

        if error:
            return jsonify({
                "errors": [{
                    "code": str(codigo),
                    "message": "Datos inválidos para la creación de un plato",
                    "level": "error",
                    "description": error
                }]
            }), codigo


        plato = datos["plato"].strip()
        precio = datos["precio"]
        descripcion = datos["descripcion"].strip()
        restriccion = datos["restricciones_alimenticias"].strip()

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM menu WHERE plato = %s", (plato,))

        if cursor.fetchone():
            return jsonify({
                "errors": [{
                "code": 409,
                "message": "Conflicto",
                "level": "error",
                "description": f"Ya existe un plato con el nombre {plato}"}]
            }),409
        
        cursor.execute("INSERT INTO menu (plato, precio, descripcion, restriccion) VALUES (%s,%s,%s,%s)", (plato, precio, descripcion, restriccion))
        conn.commit()
        return "",201

    except Exception as error_interno:
            return jsonify({
                "errors": [{
                    "code": "500",
                    "message": "Error interno del servidor",
                    "level": "error",
                    "description": str(error_interno)
                }]
            }), 500


    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@menu_bp.route('/<int:id>', methods=['PATCH'])
def modificar_platos_menu(id):

    conn = None
    cursor = None

    try:
        data = request.json

        if data is None:
            return jsonify({
                "errors": [{
                    "code": "400", 
                    "message": "El body no cumple con el formato JSON"
                }]
            }), 400

        tipos_datos_validos = {
            "plato": str,
            "precio": int,
            "descripcion": str,
            "restricciones_alimenticias": str
        }

        for campo, valor in data.items(): #verifico que se respete tanto el campo (su nombre) como el tipo de dato (su valor)

            if campo not in tipos_datos_validos:
                return jsonify({
                    "errors": [{
                        "code": "400", 
                        "level": "error", 
                        "description": f"El campo {campo} no es válido", 
                        "message": "Campo invalido"
                    }]
                }), 400

            if not isinstance(valor, tipos_datos_validos[campo]):
                return jsonify({
                    "errors": [{
                        "code": "400", 
                        "level": "error", 
                        "description": f"El campo '{campo}' debe ser de tipo {tipos_datos_validos[campo].__name__}", 
                        "message": "Tipo de dato invalido"
                    }]
                }), 400


        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM menu WHERE id = %s", (id, ))
        if not cursor.fetchone():

            return jsonify({
            "errors": [{ 
                "code": "404",
                "level": "error",
                "message": "Plato a modificar no encontrado",
                "description": f"El plato cuyo ID es: {id} no existe en la base de datos."
            }]
            }), 404
        
        campos = []
        valores = []

        for campo, valor in data.items():
            campos.append(f"{campo} = %s")
            valores.append(valor)
        
        valores.append(id)

        if campos:
            query = "UPDATE menu SET " + ", ".join(campos) + " WHERE id = %s"
        
        cursor.execute(query, valores)
        conn.commit()

        return '', 204
    
    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": str(error_interno)
            }]
        }), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@menu_bp.route('/menu/<int:id>', methods=['DELETE'])
def borrar_plato_menu(id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM menu WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "Plato no encontrado",
                    "level": "error",
                    "description": f"No existe un plato con id {id}"
                }]
            }), 404

        cursor.execute("DELETE FROM menu WHERE id = %s", (id,))
        conn.commit()
        return "", 204

    except Exception as error_interno:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": str(error_interno)
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
