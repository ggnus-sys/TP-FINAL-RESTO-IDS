
from flask import Flask,jsonify,request, Blueprint
from ..db import get_connection
from ..validators.menu import validar_body_menu

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/', methods=['GET'])
def buscar_platos_menu():

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    id_plato_base = request.args.get('id') #me lo dan como string, lo convierto a integer 
    id_plato = None 
    nombre_plato = request.args.get('plato')
    restricciones = request.args.getlist('restricciones_alimenticias')
    

#verificaciones sin conexion a db

    if id_plato_base is not None:
        try:
            id_plato = int(id_plato_base)
        except ValueError:
            return jsonify({
                "errors": [{
                    "code": "400", 
                    "message": "Parámetro erróneo", 
                    "level": "error", 
                    "description": "El id debe ser un entero."
                }]
            }), 400

        if id_plato <= 0:
            return jsonify({
                "errors": [{
                    "code": "400", 
                    "message": "Parámetro erróneo", 
                    "level": "error", 
                    "description": "El id debe ser un entero positivo."
                }]
            }), 400

    if restricciones: 
        for restriccion in restricciones:
            if restriccion not in RESTRICCIONES_VALIDAS:
                return jsonify({"errors": [{"code": "400", "message": "Parámetro erróneo", "level": "error", "description": f"La restricción '{restriccion}' no es válida."}]}), 400

    query = "SELECT * FROM menu"
    filtros = []
    params = []

    if id_plato:
        filtros.append("id = %s")
        params.append(id_plato)

    if nombre_plato:
        filtros.append("plato LIKE %s")
        params.append(f"%{nombre_plato}%")      # %pizza% → contiene "pizza" sintaxis SQL

    for restriccion in restricciones:
        filtros.append("FIND_IN_SET(%s, restricciones_alimenticias)")
        params.append(restriccion)

    if filtros:
        query += " WHERE " + " AND ".join(filtros) 


    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        print(query, params)
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        
        resultado_formateado = []

        for fila in resultado:
            if isinstance(fila.get('restricciones_alimenticias'), set): #como restricciones_alimenticias es tipo dato set, lo convertimos a un string con elemntos unidos por "," para que pueda se le pueda aplicar jsonify
                fila['restricciones_alimenticias'] = ",".join(fila['restricciones_alimenticias'])

            resultado_formateado.append({
                "id": fila["id"],
                "plato": fila["plato"],
                "precio": fila["precio"],
                "descripcion": fila["descripcion"],
                "restricciones_alimenticias": fila["restricciones_alimenticias"]
            })

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
        
        print(type(resultado), resultado)
        return jsonify(resultado_formateado), 200 
    
    except Exception as error_interno:
        print(type(error_interno), str(error_interno))
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

@menu_bp.route('/', methods=['POST'])
def agregar_platos_menu():
    
    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    conn = None
    cursor = None

    try:
        datos = (request.json)

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
        restriccion = datos["restricciones_alimenticias"].replace(" ", "") #deja el set como estaba, solo elimina los espacios que haya entre las comas y los elementos
        restricciones_ingresadas = restriccion.split(",") #crea una lista separando los elementos del set mediante ","

        for r in restricciones_ingresadas:
            if r not in RESTRICCIONES_VALIDAS:
                return jsonify({
                    "errors": [{
                        "code": "400",
                        "level": "error",
                        "message": "Restricción inválida",
                        "description": f"La restricción '{r}' no es válida."
                    }]
                }), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary = True)
        
        cursor.execute("SELECT id FROM menu WHERE plato = %s", (plato,))

        if cursor.fetchone():
            return jsonify({
                "errors": [{
                "code": 409,
                "message": "Conflicto",
                "level": "error",
                "description": f"Ya existe un plato con el nombre {plato}"}]
            }),409
        
        cursor.execute("INSERT INTO menu (plato, precio, descripcion, restricciones_alimenticias) VALUES (%s,%s,%s,%s)", (plato, precio, descripcion, restriccion))
        conn.commit()
        return "",201

    except Exception as error_interno:
            print(type(error_interno), error_interno)
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

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    conn = None
    cursor = None


    try:
        datos = request.get_json(silent=True) #si no se puede convertir a json, devuelve None 

        if datos is None:
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

        for campo, valor in datos.items(): #verifico que se respete tanto el campo (su nombre) como el tipo de dato (su valor)

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
            
            if campo == "precio" and valor <= 0:
                return jsonify({
                    "errors": [{
                        "code": "400",
                        "level": "error",
                        "message": "Precio inválido",
                        "description": "El precio debe ser mayor a 0."
                    }]
                }), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

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

        for campo, valor in datos.items():

            if campo == "restricciones_alimenticias":
                valor = valor.replace(" ", "")
                restricciones_ingresadas = valor.split(",")#guarda en una lista los elementos (separados por ",") del set restricciones_alimenticias
                for r in restricciones_ingresadas:
                    if r not in RESTRICCIONES_VALIDAS:
                        return jsonify({
                            "errors": [{
                                "code": "400",
                                "level": "error",
                                "message": "Restricción inválida",
                                "description": f"La restricción '{r}' no es válida."
                            }]
                        }), 400
                    
            campos.append(f"{campo} = %s")
            valores.append(valor)
            
        valores.append(id)
                        

        if campos:
            query = "UPDATE menu SET " + ",".join(campos) + " WHERE id = %s"
        
        print(query, valores)
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

@menu_bp.route('/<int:id>', methods=['DELETE'])
def borrar_plato_menu(id):
    conn = None
    cursor = None

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
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

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
