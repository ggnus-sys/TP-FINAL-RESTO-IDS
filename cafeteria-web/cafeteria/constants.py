import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = 'http://backend:5000/kaifer-api' #para conexion entre servicios(entre contenedores)
API_BASE_URL_HOST_MACHINE= 'http://localhost:5000/kaifer-api' #acceder a la API desde el host local, no docker

# Validaciones para el formulario de reseñas
CALIF_MIN = 1
CALIF_MAX = 5

#Capacidad maxima de mesas de la web
CAPACIDAD_MAX_WEB = 15

#CANTIDAD_MAX_RESERVAS_USUARIO
CAPACIDAD_MAX_RESERVAS_USUARIO = 3

#Tiempo maximo de un cliente dentro de la cafeteria
DURACION_TURNO = timedelta(minutes=90)