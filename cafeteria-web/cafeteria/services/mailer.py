import logging
from flask import abort, render_template, current_app, send_file
from flask_mail import Mail, Message
from ..constants import API_BASE_URL_HOST_MACHINE
import segno

logger = logging.getLogger(__name__)


def _enviar(asunto: str, destinatario: str, template_base: str, contexto: dict) -> None:
    """Renderiza la version HTML y la TXT del template y envia el email."""

    id_reserva = contexto.get('id_reserva')

    mensaje = Message(
        subject=asunto,
        recipients=[destinatario],
    )

    mensaje.html = render_template(f'{template_base}.html', **contexto)
    mail = Mail(current_app)

    with current_app.open_resource(f"static/images/rid{id_reserva}QR.png") as fp:
        mensaje.attach(f"rid{id_reserva}QR.png", "image/png", fp.read(), headers={'Content-ID': '<image1>'})

   
    mail.send(mensaje)

    logger.info(f"Email '{asunto}' enviado a {destinatario} (template: {template_base})")

def enviar_qr_confirmacion_reserva(usuario: dict, expira_en: str, id_reserva: int) -> None:
    """Manda el email con el link para confirmar la reserva, que incluye el QR para acceder al menú."""

    _enviar(
        asunto='QR de confirmación de tu reserva',
        destinatario=usuario['email'],
        template_base='qr-confirmacion-reserva',
        contexto={
            'usuario':   usuario,
            'id_reserva':    id_reserva,
            'expira_en': expira_en,
            'link': f"{API_BASE_URL_HOST_MACHINE}/reservas/{id_reserva}"
        },
    )
