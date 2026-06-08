import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)

def crear_reserva(reserva):
    try:
        response = requests.post(f'{API_BASE_URL}/reservas', json=reserva)
        if response.status_code == 201:
            return True
        
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return False

    except Exception as e:
        logger.error(f"Error al reservar mesas: {e}")
        return False
    
    return False


def obtener_reservas():
    reservas = []

    try:
        response = requests.get(f'{API_BASE_URL}/reservas')
        if response.status_code == 200:
            reservas = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener reservas: {e}")

    return reservas
