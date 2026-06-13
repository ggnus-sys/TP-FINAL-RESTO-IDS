import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_servicios_extra() -> list[dict]:
    """Consume el endpoint del backend para obtener los datos del menú."""
    servicios_extra = []

    try:
        response = requests.get(f'{API_BASE_URL}/servicios_extra')
        if response.status_code == 200:
            servicios_extra = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener menú: {e}")

    return servicios_extra

def obtener_servicio_extra(servicio_extra_id: int) -> dict:
    """Consume el endpoint del backend para obtener los datos de un servicio extra específico."""
    try:
        response = requests.get(f'{API_BASE_URL}/servicios_extra/{servicio_extra_id}')
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error al obtener servicio extra: {response.status_code}")
            return {}
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {}
    except Exception as e:
        logger.error(f"Error al obtener servicio extra: {e}")
        return {}

def agregar_servicio_extra(servicio_extra: str, descripcion: str) -> dict:
    """Agrega un nuevo servicio extra al menú a través del endpoint del backend."""
    try:
        payload = {
            "servicio_extra": servicio_extra,
            "descripcion": descripcion,
        }
        response = requests.post(f'{API_BASE_URL}/servicios_extra', json=payload)
        return {
            "ok": response.status_code == 201,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al agregar servicio extra: {e}")
        return {
            "errores": [f"Error al agregar servicio extra: {e}"]
        }
    
def borrar_servicio_extra(servicio_extra_id: int) -> dict:
    """Elimina un servicio_extra del menú a través del endpoint del backend."""
    try:
        response = requests.delete(f'{API_BASE_URL}/servicios_extra/{servicio_extra_id}')
        return {
            "ok": response.status_code == 200,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al eliminar servicio extra: {e}")
        return {
            "errores": [f"Error al eliminar servicio extra: {e}"]
        }

def modificar_servicio_extra(servicio_extra_id: int, servicio_extra: str, descripcion: str) -> dict:
    """Modifica un servicio_extra del menú a través del endpoint del backend."""
    try:
        payload = {
            "servicio_extra": servicio_extra,
            "descripcion": descripcion,
        }
        response = requests.patch(f'{API_BASE_URL}/servicios_extra/{servicio_extra_id}', json=payload)
        return {
            "ok": response.status_code == 200,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al modificar servicio extra: {e}")
        return {
            "errores": [f"Error al modificar servicio extra: {e}"]
        }