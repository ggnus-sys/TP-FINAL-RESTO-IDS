import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_menu() -> list[dict]:
    """Consume el endpoint del backend para obtener los datos del menú."""
    menu = []

    try:
        response = requests.get(f'{API_BASE_URL}/menu')
        if response.status_code == 200:
            menu = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener menú: {e}")

    return menu

def obtener_plato(plato_id: int) -> dict:
    """Consume el endpoint del backend para obtener los datos de un plato específico."""
    try:
        response = requests.get(f'{API_BASE_URL}/menu/{plato_id}')
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error al obtener plato: {response.status_code}")
            return {}
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {}
    except Exception as e:
        logger.error(f"Error al obtener plato: {e}")
        return {}

def agregar_plato(plato: str, precio: int, descripcion: str, restricciones: str) -> dict:
    """Agrega un nuevo plato al menú a través del endpoint del backend."""
    try:
        payload = {
            "plato": plato,
            "precio": precio,
            "descripcion": descripcion,
            "restricciones_alimenticias": restricciones
        }
        response = requests.post(f'{API_BASE_URL}/menu', json=payload)
        return {
            "ok": response.status_code == 201,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al agregar plato: {e}")
        return {
            "errores": [f"Error al agregar plato: {e}"]
        }
    
def borrar_plato(plato_id: int) -> dict:
    """Elimina un plato del menú a través del endpoint del backend."""
    try:
        response = requests.delete(f'{API_BASE_URL}/menu/{plato_id}')
        return {
            "ok": response.status_code == 200,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al eliminar plato: {e}")
        return {
            "errores": [f"Error al eliminar plato: {e}"]
        }

def modificar_plato(plato_id: int, plato: str, precio: int, descripcion: str, restricciones: str) -> dict:
    """Modifica un plato del menú a través del endpoint del backend."""
    try:
        payload = {
            "plato": plato,
            "precio": precio,
            "descripcion": descripcion,
            "restricciones_alimenticias": restricciones
        }
        response = requests.patch(f'{API_BASE_URL}/menu/{plato_id}', json=payload)
        return {
            "ok": response.status_code == 200,
        }

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")
        return {
            "errores": ["No se pudo conectar con la API."]
        }

    except Exception as e:
        logger.error(f"Error al modificar plato: {e}")
        return {
            "errores": [f"Error al modificar plato: {e}"]
        }