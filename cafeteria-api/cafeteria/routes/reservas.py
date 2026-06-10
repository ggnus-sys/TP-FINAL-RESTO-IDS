from flask import Blueprint, jsonify, request
from ..services.reservas import listar_reservas, crear_reserva, quitar_reserva
from ..validators.reservas import validar_body_reserva

reservas_bp = Blueprint('reservas_bp', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def obtener_reservas():

    try:
        reservas = listar_reservas()

        if not reservas:
            return '', 204
        
        return jsonify(reservas), 200
    
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500
    

@reservas_bp.route('/reservas', methods=['POST'])
def anadir_reserva(): 

    datos = request.get_json()
    error, codigo = validar_body_reserva(datos) 

    if error:
        return jsonify({"errors": [{"code": str(codigo), "message": "Datos inválidos", "level": "error", "description": error}]}), codigo

    try:
        id_reserva = crear_reserva(datos)
        return jsonify({
            "id": id_reserva}
            ), 201

    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Conflicto", "level": "error", "description": mensaje}]}), status

    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500
    


@reservas_bp.route('/reservas/<int:id>', methods=['DELETE'])
def eliminar_reserva(id):

    if id <= 0:
        return jsonify({"errors": [{"code": "400", "message": "Parámetro inválido", "level": "error", "description": "El id debe ser un entero positivo"}]}), 400

    try:
        quitar_reserva(id)
        return '', 204
    
    except ValueError as e:
        mensaje, status = e.args[0], e.args[1]
        return jsonify({"errors": [{"code": str(status), "message": "Error", "level": "error", "description": mensaje}]}), status
    
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500


