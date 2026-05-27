import os, re
from dotenv import load_dotenv

load_dotenv()

# URL base de la API
BASE_URL = '/kaifer-api'

# Formato de fecha esperado por la API
FORMATO_FECHA = '%Y-%m-%d'

#Validación mail
EMAIL_REGEX = re.compile(r'^[^@]+@[^@]+\.[^@]+$')

#Roles de usuario
ROLES_VALIDOS = ("admin","cliente")

# Reglas de dominio
MIN_CALIFICACION = 1
MAX_CALIFICACION = 5

# Configuracion de la base de datos MySQL (levantada via docker-compose)
DB_HOST     = os.getenv('DB_HOST', 'mysql')
DB_PORT     = int(os.getenv('DB_PORT', '3306'))
DB_USER     = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME     = os.getenv('DB_NAME', 'kaifer_db')
DB_URL      = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Codigos de error
ERROR_CODE_INVALID_BODY        = 'invalid.body'
ERROR_CODE_INVALID_MIN_VALUE   = 'invalid.min.value'
ERROR_CODE_INVALID_MAX_VALUE   = 'invalid.max.value'
ERROR_CODE_ALUMNO_NOT_FOUND    = 'alumno.not.found'
ERROR_CODE_MATERIA_NOT_FOUND   = 'materia.not.found'