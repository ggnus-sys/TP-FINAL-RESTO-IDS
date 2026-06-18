from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.reservas import crear_reserva, obtener_reservas, confirmar_reserva, cancelar_reserva
from ..services.mailer import enviar_qr_confirmacion_reserva
from ..constants import API_BASE_URL_HOST_MACHINE, CAPACIDAD_MAX_WEB, CAPACIDAD_MAX_RESERVAS_USUARIO
from ..utils import requiere_login, usuario_actual, obtener_mesas_ocupadas_franja, obtener_cantidad_reservas_logueado
import segno
reservas_bp = Blueprint('reservas_bp', __name__)


@reservas_bp.route('/reservas', methods=['GET','POST'])
@requiere_login()
def reservas():
    if request.method == 'POST':
        usuario_logueado = usuario_actual()

        id_usuario = usuario_logueado['id']
        mesas = int(request.form.get("mesas"))
        fecha_dia = request.form.get("fecha_dia")   
        fecha_hora = request.form.get("fecha_hora")
        errores = []

        if not id_usuario:
            errores.append("Debe ingresar un ID valido para solicitar una reserva.")

        if not fecha_dia or not fecha_hora:
            errores.append("Debe seleccionar el dia y la hora de la reserva.")

        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('reservas_bp.reservas'))
        

        fecha_completa = fecha_dia + " " + fecha_hora

        mesas_ya_reservadas = obtener_mesas_ocupadas_franja(fecha_completa) 

        if mesas_ya_reservadas + mesas > CAPACIDAD_MAX_WEB:
            mesas_libres = CAPACIDAD_MAX_WEB - mesas_ya_reservadas
            if mesas_libres <= 0:
                errores.append(f"Ya no quedan mesas disponibles para las {fecha_hora}.")
            else:
                errores.append(f"Solo quedan {mesas_libres} mesas disponibles para esa hora.")

        reservas_usuario_logueado = obtener_cantidad_reservas_logueado(id_usuario)

        if reservas_usuario_logueado >= CAPACIDAD_MAX_RESERVAS_USUARIO:
            errores.append(f"No puedes tener más de 3 reservas pendientes simultaneamente.")

        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('reservas_bp.reservas'))
        

        body = { "id_usuario": id_usuario,
                "mesas": mesas,
                "fecha_reserva": fecha_completa,
                "estado_reserva" : 'pendiente'}
        
        resultado : int = crear_reserva(body)

        if resultado:
            flash("Reserva hecha con exito.", 'success')
            qrcode = segno.make(f"{API_BASE_URL_HOST_MACHINE}/confirmar-reserva?reserva_id={resultado}")
            qrcode.save(f'static/images/rid{resultado}QR.png', scale=5)
            enviar_qr_confirmacion_reserva(
                usuario={
                    'id': id_usuario,
                    'nombre': usuario_logueado['nombre'],
                    'email': usuario_logueado['email']
                },
                expira_en = fecha_completa,
                id_reserva=resultado
            )
        else:
            flash('Error al reservar.' , 'error')

        return redirect(url_for('reservas_bp.reservas'))

    return render_template('reservation.html')



@reservas_bp.route('/confirmar-reserva', methods=['GET'])
@requiere_login()
def confirmacion_reserva():
    id_reserva = request.args.get('reserva_id', type=int)
    if not id_reserva:
        flash('Reserva inválida', 'error')
        return redirect(url_for('reservas_bp.reservas'))

    if confirmar_reserva(id_reserva):
        flash('Reserva confirmada con éxito', 'success')
    else:
        flash('Error al confirmar la reserva', 'error')

    return redirect(url_for('reservas_bp.reservas'))


@reservas_bp.route('/cancelar-reserva', methods=['GET', 'POST'])
@requiere_login()
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
        return redirect(url_for('reservas_bp.reservas'))

    return render_template('cancel_reservation.html', id_reserva=id_reserva)