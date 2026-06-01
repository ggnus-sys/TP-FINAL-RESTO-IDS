from flask import Blueprint, jsonify, render_template, request
#from ..services.reservas import listar_reservas, crear_reserva, quitar_reserva

reservas_bp = Blueprint('reservas_bp', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def reservas():
    return render_template('reservation.html')