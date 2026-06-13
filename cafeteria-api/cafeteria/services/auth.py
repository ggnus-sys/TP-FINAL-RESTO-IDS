# la idea de auth es mantener la lógica detras del manejo de endpoints que van a estar en routes
# TODO: despueés borrar este mensaje, es para explicar la idea nomas
from ..db import obtener_usuario_por_email
from ..validators.usuarios import validar_body_usuario, validar_body_login
from ..utils import generar_jwt, verificar_password, construir_error_api
from .usuarios import construir_usuario_dto, crear_usuario


# -------------registro ------------------------

def registrar_usuario(body: dict):
    """registra un nuevo usuario en la base de datos, devuelve el dto"""
    error, codigo = validar_body_usuario(body)
    if error:
        raise ValueError(error, codigo)
    
    if obtener_usuario_por_email(body["email"]):
        raise ValueError(construir_error_api(
        code='ERROR_CODE_EMAIL_YA_REGISTRADO',
        message='Email ya registrado',
        description='Ya existe un usuario con ese email'), 409)
    
    crear_usuario(body)

    return construir_usuario_dto(obtener_usuario_por_email(body["email"])) #dista un toque de lo de leo pero así debería andar bien!!
    
# ------------- login (de toda la vida) ------------------

def login_usuario(body: dict):
    """verifica un usuario y contraseña, devuelve dto y token"""
    error, codigo = validar_body_login(body)
    if error:
        raise ValueError(error, codigo)
    
    usuario = obtener_usuario_por_email(body["email"])

    if not usuario or not verificar_password(body["password"], usuario["contrasena"]):
        raise ValueError(construir_error_api(
            code='invalid.credentials',
            message='Credenciales inválidas',
            description='El email o la contraseña son incorrectos'
        ), 401)
    
    return {
        'usuario' : construir_usuario_dto(usuario),
        'token' : generar_jwt(usuario['id'], usuario['rol'])
    }