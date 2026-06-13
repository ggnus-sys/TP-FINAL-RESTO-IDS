from functools import wraps
from flask import session, redirect, url_for, flash

#la idea de utils es contener las funciones que guardan el JWT y los datos del usuario en una sesion

def usuario_actual():
    """Retorna el usuario logueado guardado en la sesion, o {} si no hay."""
    return session.get('usuario') or {}


def token_actual():
    """Retorna el JWT guardado en la sesion, o cadena vacia si no hay."""
    return session.get('token') or ''


def guardar_sesion(token: str, usuario: dict):
    """Persiste token y usuario en la sesion de Flask."""
    session['token']   = token
    session['usuario'] = usuario


def limpiar_sesion():
    """Borra todos los datos de autenticacion de la sesion."""
    session.pop('token', None)
    session.pop('usuario', None)


def requiere_login(rol=None):
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):

            if not usuario_actual() or not token_actual():
                flash('Iniciá sesión para continuar.', 'error')
                return redirect(url_for('auth.login'))
            
            if rol and usuario_actual()['rol'] != rol:
                flash('No tenes permiso para acceder a esta página','error')
                return redirect(url_for('index'))
                
            
            return funcion(*args, **kwargs)
        return wrapper
    return decorador