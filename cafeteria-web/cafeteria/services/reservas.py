import logging
import requests
import segno
from .mailer import enviar_qr_confirmacion_reserva
from ..constants import API_BASE_URL, DURACION_TURNO, CAPACIDAD_MAX_WEB, CAPACIDAD_MAX_RESERVAS_USUARIO, API_BASE_URL_HOST_MACHINE
from datetime import datetime

logger = logging.getLogger(__name__)

def crear_reserva(reserva, token):
    try:
        headers = { "Authorization": f"Bearer {token}" }
        response = requests.post(f'{API_BASE_URL}/reservas', json=reserva, headers = headers)
        
        if response.status_code == 201:
            return response.json().get("id"), None
        else:
            data_error = response.json()
            
            if "errors" in data_error and len(data_error["errors"]) > 0:
                mensaje_error = data_error["errors"][0].get("description", "Error sin descripción.")
            else:
                mensaje_error = "Error desconocido en el servidor."
                
            return None, mensaje_error
        
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al reservar mesas: {e}")
    
    return False, None


def obtener_reservas(token, fecha_especifica = None, usuario_especifico = None, estado = None):
    reservas = []

    try:
        
        headers = { "Authorization": f"Bearer {token}" }
        filtros = {
            'fecha_especifica': fecha_especifica,
            'id_usuario': usuario_especifico,
            'estado': estado
        }
        
        filtros_no_nulos = {k: v for k, v in filtros.items() if v is not None}
        
        
        response = requests.get(f'{API_BASE_URL}/reservas', params=filtros_no_nulos, headers = headers)
        
        if response.status_code == 200:
            reservas = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener reservas: {e}")

    return reservas

def confirmar_reserva(id_reserva):
    try:
        response = requests.patch(
            f'{API_BASE_URL}/reservas/{id_reserva}',
            json={"estado": "confirmada"}
        )
        return response.status_code == 204

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
    except Exception as e:
        logger.error(f"Error al confirmar reserva: {e}")
    
    return False


def cancelar_reserva(id_reserva):
    try:
        response = requests.patch(
            f'{API_BASE_URL}/reservas/{id_reserva}',
            json={"estado": "cancelada"}
        )
        return response.status_code == 204

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
    except Exception as e:
        logger.error(f"Error al cancelar reserva: {e}")

    return False


    

def procesar_notificacion_reserva(id_reserva, usuario, fecha_completa):
    qrcode = segno.make(f"{API_BASE_URL_HOST_MACHINE}/confirmar-reserva?reserva_id={id_reserva}")
    qrcode.save(f'static/images/rid{id_reserva}QR.png', scale=5)
        
    enviar_qr_confirmacion_reserva(
        usuario=usuario,
        expira_en=fecha_completa,
        id_reserva=id_reserva
    )


def registrar_nueva_reserva(usuario_logueado, mesas, fecha_dia, fecha_hora, token):
    
    if not fecha_dia or not fecha_hora or not fecha_dia.strip() or not fecha_hora.strip():
        return ["El campo dia y hora no pueden estar vacíos"], "error"

    fecha_completa = fecha_dia + " " + fecha_hora

    id_usuario = usuario_logueado["id"]

    body = {"id_usuario": id_usuario,
            "mesas": mesas,
            "fecha_reserva": fecha_completa,
            "estado_reserva" : 'pendiente'
    }
        
    id_reserva, error = crear_reserva(body, token)

    if id_reserva:

        datos_usuario = {
            'id': id_usuario,
            'nombre': usuario_logueado['nombre'],
            'email': usuario_logueado['email']
        }
        
        procesar_notificacion_reserva(id_reserva, datos_usuario, fecha_completa)
        return ["Reserva hecha con éxito."], "success"
            
    mensaje_final = error if error else "Error al reservar."
    return [mensaje_final], "error"
