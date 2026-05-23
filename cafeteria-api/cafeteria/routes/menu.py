
from flask import Flask,jsonify,request
from db import get_connection



def validar_body_menu(cuerpo):

    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    plato = cuerpo.get("plato")
    precio = cuerpo.get("precio")
    descripcion = cuerpo.get("descripcion")
    restriccion = cuerpo.get("restriccion_alimenticia")
    
    if plato is None or precio is None or descripcion is None or restriccion is None:
        return "Faltan campos por asignar",400

    if (not isinstance(plato,str)) or (not isinstance(precio,int)) or (precio <= 0) or (not isinstance(descripcion,str)) or (not isinstance(restriccion,str)):
        return "El nombre del plato, su descripción y la restricción alimenticia (si abarca alguna) deben ser de tipo string. El precio debe ser de tipo integer y mayor a 0",400

    return None, None

@app.route('/menu', methods=['GET'])
def buscar_platos_menu():

    RESTRICCIONES = ["vegano", "celiaco", "vegetariano"] 

    nombre = request.args.get('nombre')
    restriccion = request.args.get('restriccion')

    if (restriccion) and (restriccion not in RESTRICCIONES):

        return jsonify({

            "errors": [{
                "code": "400",
                "message": "Parámetro desconocido",
                "level" : "error",
                "description": f"La restricción alimenticia '{restriccion}' no es válida para busqueda."
            }]
        }), 400


    query = "SELECT * FROM menu"
    filtros = []
    params = []

    if nombre:
        filtros.append("plato LIKE %s")
        params.append(f"%{nombre}%")      # %pizza% → contiene "pizza" sintaxis SQL

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
        if (not resultado) and (nombre): 
            return jsonify({
                "errors": [{
                    "code": "404", 
                    "message": "Plato no encontrado", 
                    "level" : "error",
                    "description": f"No hay registros del menu para el plato '{nombre}'."
                }]
            }), 404

        return jsonify(resultado), 200 
    except Exception as error_interno:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(error_interno)}]}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/menu', methods=['POST'])
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


        plato = datos["plato"]
        precio = datos["precio"]
        descripcion = datos["descripcion"]
        restriccion = datos["restriccion_alimenticia"]

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
