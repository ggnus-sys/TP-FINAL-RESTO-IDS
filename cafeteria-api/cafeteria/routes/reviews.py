from flask import Blueprint, Flask, request, jsonify
from ..db import get_connection


reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/resenas', methods=['GET'] )
def listar_resenas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary= True)

        #agarra todas las reseñas de la base de datos
        cursor.execute("SELECT * FROM resenas")
        resultado= cursor.fetchall()
        
        #si no existe ninguna reseñas devuelve error
        if not resultado:
            return jsonify ({"errors":[{"code" : "404", "Message":"No hay reseñas", "level": "Error","Description":"reseñas no encontradas" }]}),404
        #esto devuelve en manera de diccionario segun esta escrito en la base de datos
        return jsonify(resultado),200  
    #a cualquier error no esperado le suelta este mensaje   
    #str(e) devuelve en formato json el mensaje de error propio de la pagina 
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@reviews_bp.route('/resenas/<int:id>', methods=['GET'])
def filtrar_resenas(id):
    try:
        conn = get_connection()
        cursor= conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM resenas WHERE id = %s",(id,))
        resultado= cursor.fetchone()

        if resultado is None:
            return jsonify ({"errors":[{"code" : "404", "Message": "No existe esa reseña", "level": "Error", "Description": "ID no encontrado"}]}), 404
        return jsonify(resultado),200
    except Exception as e:
        return jsonify ({"errors":[{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@reviews_bp.route('/resenas', methods=['POST'])
def crear_resena():
    try:
        datos = request.get_json()
        if datos is None:
            return jsonify({"errors": [{"code": "400", "message": "Datos inválidos"}]}), 400
        contenido = datos.get("contenido")
        estrellas = datos.get("estrellas")
        id_usuario = datos.get("id_usuario")
        if not contenido or not estrellas or not id_usuario:
            return jsonify({"errors":[{"code": 400, "message":"Datos insuficientes", "level": "error", "description": "Faltan datos"}]})
        if estrellas not in range (1,6):
            return jsonify({"errors": [{"code": "400", "message": "Las estrellas deben ser entre 1 y 5"}]}), 400
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({"errors": [{"code": "404", "message": "El usuario no existe"}]}), 404
        
        cursor.execute("INSERT INTO resenas (contenido, estrellas, id_usuario) VALUES (%s,%s,%s)",(contenido, estrellas, id_usuario))
        conn.commit()
        return "",201
    except Exception as e:
        return jsonify ({"errors":[{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@reviews_bp.route('/resenas/<int:id_resena>', methods=['DELETE'])
def eliminar_resena(id_resena):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from resenas WHERE id= %s",(id_resena,))
        resultado = cursor.fetchone()
        if resultado is None:
            return jsonify ({"errors":[{"code" : "404", "Message": "No existe esa reseña", "level": "Error", "Description": "ID no encontrado"}]}), 404
        cursor.execute("DELETE from resenas WHERE id = %s",(id_resena,))
        conn.commit()
        return "", 204
    
    except Exception as e:
        return jsonify ({"errors":[{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reviews_bp.route('/resenas/<int:id_resena>',methods=['PATCH'])
def actualizar_resena(id_resena):
    try:
        datos = request.get_json()
        if datos is None:
            return jsonify({"error": "Datos inválidos"}), 400
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resenas WHERE id = %s", (id_resena,))
        resultado = cursor.fetchone()
        if resultado is None:
            return jsonify({"errors": [{"code": "404", "message": "Reseña no encontrada"}]}), 404
        campos = []
        valores = []
        if "contenido" in datos:
            campos.append("contenido = %s")
            valores.append(datos["contenido"])
        if "estrellas" in datos:
            campos.append("estrellas = %s")
            valores.append(datos["estrellas"])
        if not campos:
            return jsonify({"errors": [{"code": "400", "message": "No se enviaron campos para actualizar"}]}), 400
        valores.append(id_resena)
        cursor.execute(f"UPDATE resenas SET {', '.join(campos)} WHERE id = %s", valores)
        conn.commit()
        return "", 204
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "description": str(e)}]}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
