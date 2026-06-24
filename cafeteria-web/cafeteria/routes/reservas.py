from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.reservas import registrar_nueva_reserva, confirmar_reserva, cancelar_reserva, obtener_reservas
from ..utils import requiere_login, usuario_actual, validar_string_no_vacio, token_actual


reservas_bp = Blueprint('reservas_bp', __name__)


@reservas_bp.route('/reservas', methods=['GET','POST'])
@requiere_login()
def reservas():
    
    if request.method == 'POST':
        usuario_logueado = usuario_actual()
        mesas = int(request.form.get("mesas"))
        fecha_dia = request.form.get("fecha_dia")   
        fecha_hora = request.form.get("fecha_hora")
        
        mensajes, categoria = registrar_nueva_reserva(usuario_logueado, mesas, fecha_dia, fecha_hora, token_actual())
        
        for mensaje in mensajes:
            flash(mensaje, categoria)

        return redirect(url_for('reservas_bp.reservas'))

    return render_template('reservation.html')

@reservas_bp.route('/confirmar-reserva', methods=['GET', 'POST'])
def confirmacion_reserva():
    id_reserva = request.args.get('reserva_id', type=int)
    if not id_reserva:
        flash('Reserva inválida', 'error')
        return redirect(url_for('reservas_bp.reservas'))

    if request.method == 'POST':
        if confirmar_reserva(id_reserva):
            flash('Reserva confirmada con éxito', 'success')
        else:
            flash('Error al confirmar la reserva', 'error')
        return render_template('confirm_reservation.html', id_reserva=id_reserva)

    return render_template('confirm_reservation.html', id_reserva=id_reserva)

@reservas_bp.route('/cancelar-reserva', methods=['GET', 'POST'])
def cancelacion_reserva():
    id_reserva = request.args.get('reserva_id', type=int)
    if not id_reserva:
        flash('Reserva inválida', 'error')
        return redirect(url_for('reservas_bp.reservas'))

    if request.method == 'POST':
        if cancelar_reserva(id_reserva):
            flash('Reserva cancelada con éxito', 'success')
        else:
            flash('Error al cancelar la reserva', 'error')
        return render_template('cancel_reservation.html', id_reserva=id_reserva)

    return render_template('cancel_reservation.html', id_reserva=id_reserva)

