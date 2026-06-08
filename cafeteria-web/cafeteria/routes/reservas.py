from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.reservas import crear_reserva, obtener_reservas
reservas_bp = Blueprint('reservas_bp', __name__)


@reservas_bp.route('/reservas', methods=['GET','POST'])
def reservas():
    if request.method == 'POST':
        id_usuario = int(request.form.get("id_usuario"))
        mesas = int(request.form.get("mesas"))
        fecha = request.form.get("fecha")

        errores = []

        if not id_usuario:
            errores.append("Debe ingresar un ID valido para solicitar una reserva.")

        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('reservas_bp.reservas'))
        
        body = { "id_usuario": id_usuario,
                "mesas": mesas,
                "fecha_reserva": fecha,
                "estado" : 'pendiente'}
        
        resultado = crear_reserva(body)

        if resultado:
            flash("Reserva hecha con exito.", 'success')
        else:
            flash('Error al reservar.' , 'error')

        return redirect(url_for('reservas_bp.reservas'))

    return render_template('reservation.html')