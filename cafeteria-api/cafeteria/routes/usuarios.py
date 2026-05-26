from flask import Blueprint, jsonify, request
from ..services.usuarios import listar_usuarios, crear_usuario, eliminar_usuario
from ..validators.usuarios import validar_body_usuario

usuarios_bp = Blueprint('usuarios_bp', __name__)

#asi queda todo bastante más limpito, salvo por los mensajes de error

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():

    try:
        usuarios = listar_usuarios()

        if not usuarios:
            return '', 204
        
        return jsonify(usuarios), 200
    
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500
    


@usuarios_bp.route('/usuarios', methods=['POST'])
def post_usuario():

    datos = request.get_json()
    error, codigo = validar_body_usuario(datos) 

    if error:
        return jsonify({"errors": [{"code": str(codigo), "message": "Datos inválidos", "level": "error", "description": error}]}), codigo

    try:
        crear_usuario(datos)
        return '', 201
    
    except ValueError as e:
        #mensaje y codigo(status) del error 
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Conflicto", "level": "error", "description": mensaje}]}), status

    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500


@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):

    if id <= 0:
        return jsonify({"errors": [{"code": "400", "message": "Parámetro inválido", "level": "error", "description": "El id debe ser un entero positivo"}]}), 400

    try:
        eliminar_usuario(id)
        return '', 204
    
    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Error", "level": "error", "description": mensaje}]}), status
    
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500