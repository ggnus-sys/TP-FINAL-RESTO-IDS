import logging
import requests
import segno
from .mailer import enviar_qr_confirmacion_reserva
from ..constants import API_BASE_URL, DURACION_TURNO, CAPACIDAD_MAX_WEB, CAPACIDAD_MAX_RESERVAS_USUARIO, API_BASE_URL_HOST_MACHINE
from datetime import datetime

logger = logging.getLogger(__name__)

def crear_reserva(reserva):
    try:
        response = requests.post(f'{API_BASE_URL}/reservas', json=reserva)
        
        if response.status_code == 201:
            return response.json().get("id")
        

    
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al reservar mesas: {e}")
    
    return False


def obtener_reservas(fecha_especifica = None, usuario_especifico = None):
    reservas = []

    try:
        
        if fecha_especifica:
            response = requests.get(f'{API_BASE_URL}/reservas?fecha_especifica={fecha_especifica}')
        
        elif usuario_especifico:
            response = requests.get(f'{API_BASE_URL}/reservas?id_usuario={usuario_especifico}')
        
        else:
            response = requests.get(f'{API_BASE_URL}/reservas')

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


    

def obtener_mesas_ocupadas_franja(fecha_datetime):

    nueva_reserva_inicio = fecha_datetime
    
    nueva_reserva_fin = nueva_reserva_inicio + DURACION_TURNO
    
    fecha_dia = nueva_reserva_inicio.strftime("%Y-%m-%d")
    
    reservas = obtener_reservas(fecha_especifica=fecha_dia)

    mesas_ocupadas = 0

    if reservas:
        for reserva in reservas:
            reserva_inicio = datetime.strptime(reserva['fecha_reserva'], "%a, %d %b %Y %H:%M:%S GMT")
            reserva_fin = reserva_inicio + DURACION_TURNO
            

            if nueva_reserva_inicio < reserva_fin and nueva_reserva_fin > reserva_inicio:
                mesas_ocupadas += int(reserva['mesas'])
                
    return mesas_ocupadas


def verificar_disponibilidad(fecha_str, mesas):
    conflictos = []

    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

    mesas_ocupadas = obtener_mesas_ocupadas_franja(fecha_datetime)

    if mesas_ocupadas + mesas > CAPACIDAD_MAX_WEB:
        mesas_libres = CAPACIDAD_MAX_WEB - mesas_ocupadas
        if mesas_libres <= 0:
            dia = fecha_datetime.strftime("%d/%m")
            hora = fecha_datetime.strftime("%H:%M")
            conflictos.append(f"Ya no quedan mesas disponibles para las {hora} del {dia}.")
        else:
            conflictos.append(f"Solo quedan {mesas_libres} mesas disponibles para esa hora.")

    return conflictos


def verificar_reservas_usuario(id_usuario):
    reservas_usuario = obtener_reservas(usuario_especifico=id_usuario)
    cantidad_reservas = len(reservas_usuario)

    if cantidad_reservas >= CAPACIDAD_MAX_RESERVAS_USUARIO:
        return [f"No podes tener más de 3 reservas pendientes simultaneamente."]
    
    return []

def procesar_notificacion_reserva(id_reserva, usuario, fecha_completa):
    qrcode = segno.make(f"{API_BASE_URL_HOST_MACHINE}/confirmar-reserva?reserva_id={id_reserva}")
    qrcode.save(f'static/images/rid{id_reserva}QR.png', scale=5)
        
    enviar_qr_confirmacion_reserva(
        usuario=usuario,
        expira_en=fecha_completa,
        id_reserva=id_reserva
    )


def registrar_nueva_reserva(usuario_logueado, mesas, fecha_dia, fecha_hora):
    
    if not fecha_dia or not fecha_hora or not fecha_dia.strip() or not fecha_hora.strip():
        return ["El campo dia y hora no pueden estar vacíos"], "error"

    fecha_completa = fecha_dia + " " + fecha_hora

    conflictos_disponibilidad = verificar_disponibilidad(fecha_completa, mesas)

    if conflictos_disponibilidad:
        return conflictos_disponibilidad, "error"
    
    id_usuario = usuario_logueado["id"]

    conflictos_reservas_usuario = verificar_reservas_usuario(id_usuario)

    if conflictos_reservas_usuario:
        return conflictos_reservas_usuario, "error"

    
    body = {"id_usuario": id_usuario,
            "mesas": mesas,
            "fecha_reserva": fecha_completa,
            "estado_reserva" : 'pendiente'
    }
        
    id_reserva = crear_reserva(body)

    if id_reserva:

        datos_usuario = {
            'id': id_usuario,
            'nombre': usuario_logueado['nombre'],
            'email': usuario_logueado['email']
        }
        procesar_notificacion_reserva(id_reserva, datos_usuario, fecha_completa)
        return ["Reserva hecha con éxito."], "success"
            
    return["Error al reservar."] , "error"
