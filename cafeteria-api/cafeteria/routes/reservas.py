from flask import Blueprint, jsonify, request
from ..services.reservas import listar_reservas

reservas_bp = Blueprint('reservas_bp', __name__)

@reservas_bp.route('/reservas', methods=['GET'])

def get_reservas():

    try:
        reservas = listar_reservas()

        if not reservas:
            return '', 204
        
        return jsonify(reservas), 200
    
    except Exception as e:
        return jsonify({"errors": [{"code": "500", "message": "Error interno", "level": "error", "description": str(e)}]}), 500
    
