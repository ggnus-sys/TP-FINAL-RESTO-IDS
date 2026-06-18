import logging
import requests
from ..constants import API_BASE_URL

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


def obtener_reservas(fecha_especifica = None):
    reservas = []

    try:
        
        if fecha_especifica:
            response = requests.get(f'{API_BASE_URL}/reservas?fecha_especifica={fecha_especifica}')
        
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

