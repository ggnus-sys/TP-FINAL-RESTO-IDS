from flask import Blueprint, request, jsonify
from ..services.reviews import listar_resenas, filtrar_resena, crear_resena, eliminar_resena, actualizar_resena
from ..validators.reviews import validar_body_resena_post, validar_body_resena_patch
from ..utils import requiere_auth

reviews_bp = Blueprint('reviews_bp', __name__)


@reviews_bp.route('/resenas', methods=['GET'])
def listar():
    try:
        resultado = listar_resenas()
        if not resultado: #si no existe ninguna reseña devuelve error
            return jsonify({"errors": [{"code": "404", "Message": "No hay reseñas", "level": "Error", "Description": "reseñas no encontradas"}]}), 404
        return jsonify(resultado), 200
      
    except Exception as e:   #a cualquier error no esperado le suelta este mensaje  
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500


@reviews_bp.route('/resenas/<int:id>', methods=['GET'])
def filtrar(id):
    try:
        resultado = filtrar_resena(id)
        if resultado is None:  #si no existe la reseña devuelve error
            return jsonify({"errors": [{"code": "404", "Message": "No existe esa reseña", "level": "Error", "Description": "ID no encontrado"}]}), 404
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500



@reviews_bp.route('/resenas', methods=['POST'])
@requiere_auth()
def crear():
    try:
        datos = request.get_json()
        error, codigo = validar_body_resena_post(datos)
        if error:
            return jsonify({"errors": [{"message": error}]}), codigo
        resultado, mensaje = crear_resena(datos)
        if resultado is None:
            return jsonify({"errors": [{"code": "404", "message": mensaje}]}), 404
        return "", 201
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500


#TODO: chequeo de admi
@reviews_bp.route('/resenas/<int:id_resena>', methods=['DELETE'])
@requiere_auth()
def eliminar(id_resena):
    try:
        resultado = eliminar_resena(id_resena)
        if resultado is None:
            return jsonify({"errors": [{"code": "404", "Message": "No existe esa reseña", "level": "Error", "Description": "ID no encontrado"}]}), 404
        return "", 204
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "level": "error", "description": str(e)}]}), 500


@reviews_bp.route('/resenas/<int:id_resena>', methods=['PATCH'])
def actualizar(id_resena):
    try:
        datos = request.get_json()
        error, codigo = validar_body_resena_patch(datos)
        if error:
            return jsonify({"errors": [{"message": error}]}), codigo
        resultado = actualizar_resena(id_resena, datos)
        if resultado is None:
            return jsonify({"errors": [{"code": "404", "message": "Reseña no encontrada"}]}), 404
        return "", 204
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno del servidor", "description": str(e)}]}), 500