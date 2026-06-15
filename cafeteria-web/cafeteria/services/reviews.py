import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)

def obtener_resenas() -> list[dict]:
    """Consume el endpoint del backend para obtener las resenas."""
    resenas = []

    try:
        response = requests.get(f'{API_BASE_URL}/resenas')
        print(response)
        if response.status_code == 200:
            resenas = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener resenas: {e}")

    return resenas


def eliminar_resena(id: int) -> bool:
    """Consume el endpoint del backend para eliminar una resena."""
    try:
        response = requests.delete(f'{API_BASE_URL}/resenas/{id}')
        if response.status_code == 204:
            return True # devuelve true si se eliminó, puedo poner para que salga algún mensajito como gonza sino
        
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return False

    except Exception as e:
        logger.error(f"Error al eliminar resena: {e}")
        return False
    
    return False

def crear_resena(resena: dict) -> bool:
    """Consume el endpoint del backend para crear una resena."""
    try:
        response = requests.post(f'{API_BASE_URL}/resenas', json=resena)
        if response.status_code == 201:
            return True # devuelve true si se creó, pero también puedo cambiarlo a un mensajito
        
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return False

    except Exception as e:
        logger.error(f"Error al crear resena: {e}")
        return False
    
    return False
