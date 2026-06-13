import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = 'http://backend:5000/kaifer-api' #para conexion entre servicios(entre contenedores)
API_BASE_URL_HOST_MACHINE= 'http://localhost:5000/kaifer-api' #acceder a la API desde el host local, no docker

# Validaciones para el formulario de reseñas
CALIF_MIN = 1
CALIF_MAX = 5