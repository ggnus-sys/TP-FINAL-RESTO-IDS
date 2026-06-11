from calendar import weekday
from datetime import datetime, timedelta, timezone
from re import sub
import logging
import bcrypt
from .constants import (
    ERROR_CODE_INVALID_MIN_VALUE,
    ERROR_CODE_INVALID_MAX_VALUE,
)
import jwt
from functools import wraps
from flask import request, jsonify
from .constants import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_HORAS


logger = logging.getLogger(__name__)

def construir_error_api(code: str, message: str, description: str, level: str = 'error') -> dict:
    """Construye un payload de error compatible con el resto de la API."""
    return {
        'errors': [{
            'code': code,
            'message': message,
            'level': level,
            'description': description
        }]
    }

def hashear_password(password: str) -> str:
    """Genera un hash bcrypt del password en texto plano."""
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hash_bytes.decode('utf-8')


def verificar_password(password: str, password_hash: str) -> bool:
    """Compara un password en texto plano contra un hash bcrypt."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except (ValueError, TypeError):
        return False
    
def validar_string_no_vacio(value, name : str)-> str:
    if value is None or not str(value).strip():
        raise ValueError(construir_error_api(
            code=f'required.{name}',
            message=f"Campo requerido: '{name}'",
            description='El campo no puede estar vacío y es obligatorio'
        ))
    return str(value).strip()

def validar_maximo(valor: int, maximo: int, nombre: str) -> int:
    if valor > maximo:
        logger.warning(f"Valor por encima del maximo: '{nombre}' es {valor}, maximo esperado {maximo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MAX_VALUE,
            message='Valor por encima del maximo permitido',
            description=f"El parametro '{nombre}' debe ser menor o igual a {maximo}. Se recibio: {valor}"
        ))

    return valor

def validar_minimo(valor: int, minimo: int, nombre: str) -> int:
    if valor < minimo:
        logger.warning(f"Valor por debajo del minimo: '{nombre}' es {valor}, minimo esperado {minimo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message='Valor por debajo del minimo permitido',
            description=f"El parametro '{nombre}' debe ser mayor o igual a {minimo}. Se recibio: {valor}"
        ))

    return valor


def validar_entero(numero, nombre: str = 'numero') -> int:
    valor = str(numero)
    valor_sin_letras = sub('[a-zA-Z]+', '', valor)

    try:
        return int(valor_sin_letras)
    except ValueError:
        logger.warning(f"Valor numerico invalido: '{numero}' no puede convertirse a entero")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no puede convertirse a un numero entero"
        ))

def validar_formato_fecha(fecha: str, formato: str, nombre: str = 'fecha') -> datetime:
    try:
        return datetime.strptime(fecha, formato)
    except ValueError:
        logger.warning(f"Formato de fecha invalido: '{fecha}' no cumple el formato '{formato}'")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{fecha}' no cumple el formato esperado '{formato}'"
        ))

def validar_fecha_futura(fecha_futura : datetime, fecha_pasada: datetime) -> datetime:
    mismo_año : bool = fecha_futura.year == fecha_pasada.year
    menor_mes : bool= fecha_futura.month < fecha_pasada.month
    menor_dia : bool= fecha_futura.day < fecha_pasada.day
    if mismo_año and menor_mes or (mismo_año and menor_mes and menor_dia):
        logger.warning(f"Fecha invalida: '{fecha_futura}' es anterior a '{fecha_pasada}'")

        raise ValueError(construir_error_api(
            code='invalid.fecha',
            message="Fecha invalida",
            description=f"La fecha '{fecha_futura}' no puede ser anterior a '{fecha_pasada}'"
        ))
    return fecha_futura

def validar_set(valor, conjunto_validos: set, nombre: str = 'valor'):
    if valor not in conjunto_validos:
        logger.warning(f"Valor no permitido: '{valor}' no está en el conjunto de valores válidos para '{nombre}'")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.value',
            message=f"Valor de '{nombre}' no permitido",
            description=f"El valor '{valor}' no es válido para '{nombre}'. Valores permitidos: {conjunto_validos}"
        ))
    return valor


# ---------------------CONFIGURACION JWT -------------

#esta funcion se encarga de generar un token especifico JWT en el momento de loguear un usuario
def generar_jwt(usuario_id: int, rol: str):
    """Genera un JWT firmado con id de usuario, rol y expira tras 24h"""
    ahora = datetime.now(timezone.utc)
    payload = {
        'sub': str(usuario_id),
        'rol': rol,
        'iat': ahora,
        'exp': ahora + timedelta(hours=JWT_EXP_HORAS)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

#esta funcion se encarga de decodificar un token y verificar que sea valido (mantenga su firma) o haya expirado
def decodificar_jwt(token: str):
    """decodifica un token y devuelve el payload en caso de ser valido, sino lanza excepcion"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError(construir_error_api(
            code='auth.token.expired',
            message='Token expirado',
            description='El token de autenticacion expiro. Volve a iniciar sesion.'), 401)
    except jwt.InvalidTokenError:
        raise ValueError(construir_error_api(
            code='auth.token.invalid',
            message='Token invalido',
            description='El token de autenticacion no es valido.'
        ), 401)
    

#esto va para los decoradores, todo aquel que le contenga asegura que, si no sos usuario, te tire un 401(no autenticado)
def requiere_auth():
    """
    Decorador que valida el JWT del header Authorization e inyecta
    el payload en request.usuario_actual.
    """
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            #podría ser función
            header = request.headers.get('Authorization', '')
            
            if not header.startswith('Bearer '):
                return jsonify(construir_error_api(
                code='auth.token.missing',
                message='Token de autenticacion faltante',
                description='Debe enviarse el header Authorization con el formato "Bearer <token>"'), 401)
            

            token = header[len('Bearer '):].strip()
            
            try:
                payload = decodificar_jwt(token)
            
            except ValueError as e:
                return jsonify(e.args[0]), e.args[1] if len(e.args) > 1 else 401
            
            request.usuario_actual = payload
            return funcion(*args, **kwargs)
        return wrapper
    return decorador