from ..db import get_connection
from ..utils import hashear_password


#data transfer object
def construir_usuario_dto(usuario: dict) -> dict:
    """DTO publico de un usuario (sin password_hash)."""
    return {
        'id':     usuario['id'],
        'email':  usuario['email'],
        'nombre': usuario['nombre'],
        'apellido': usuario['apellido'],
        'rol':    usuario['rol'],
    }


def listar_usuarios():
    #chequear... no debería pasar nada 
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        #esto tal vez podría modularizarse (leo usa db)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return [construir_usuario_dto(usuario) for usuario in usuarios]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def crear_usuario(datos):
    nombre = datos['nombre'].strip()
    apellido = datos['apellido'].strip()
    email = datos['email'].strip().lower()
    password = datos['password']
    rol = datos.get('rol', 'cliente')

    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        #chequeo existencia 
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            #devolucion de (mensaje, error)
            raise ValueError("El email ya está registrado",409)
        
        #hasheo de la contraseña
        hash_password = hashear_password(password)
        cursor.execute("INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, apellido, email, hash_password, rol))
        conn.commit()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def eliminar_usuario(id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id,))

        #chequeo existencia
        if not cursor.fetchone():
            raise ValueError(f"No existe un usuario con id {id}", 404)

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()

    finally:
        if cursor: 
            cursor.close()
        if conn: 
            conn.close()