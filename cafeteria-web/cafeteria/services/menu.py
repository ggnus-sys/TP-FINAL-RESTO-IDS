import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_menu() -> list[dict]:
    """Consume el endpoint del backend para obtener los datos de un menú por ID."""
    menu = []

    try:
        response = requests.get(f'{API_BASE_URL}/menu')
        print(response)
        if response.status_code == 200:
            menu = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener menú: {e}")

    return menu

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
