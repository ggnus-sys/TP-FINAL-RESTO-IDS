from sqlalchemy import create_engine, text
from .constants import DB_URL, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector
# Motor de conexion compartido por toda la aplicacion.
# El pool de conexiones lo maneja SQLAlchemy automaticamente.
motor = create_engine(DB_URL, pool_pre_ping=True)



def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ---------------------------------------------------------------
# Funciones de soporte
# ---------------------------------------------------------------

def fila_a_dict(fila) -> dict:
    """Convierte una fila del resultado de una query en un diccionario."""
    return dict(fila._mapping)


def ejecutar_consulta(sql: str, parametros: dict = None) -> list[dict]:
    """Ejecuta una SELECT y devuelve todas las filas como lista de dicts."""
    with motor.connect() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})

        return [fila_a_dict(fila) for fila in resultado]
    

def obtener_usuario_por_email(email: str):
    """obtiene un usuario por su email, o None si no existe."""
    sql = "SELECT * FROM usuarios WHERE email = :email"
    usuarios = ejecutar_consulta(sql, {"email": email})

    if usuarios:
        return usuarios[0]
    else:
        return None