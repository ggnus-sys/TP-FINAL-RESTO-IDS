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