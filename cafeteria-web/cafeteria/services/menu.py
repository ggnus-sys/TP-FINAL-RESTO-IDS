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
