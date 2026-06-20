from ..db import get_connection
from..constants import FORMATO_FECHA, CANTIDAD_MAX_RESERVAS_USUARIO
from ..utils import construir_error_api
from datetime import datetime


def mensaje_reserva(reserva):
    return {
        'id':   reserva['id'],
        'id_usuario':   reserva['id_usuario'],
        'mesas':    reserva['mesas'],
        'fecha_creacion':   reserva['fecha_creacion'],
        'fecha_reserva':    reserva['fecha_reserva'],
        'estado_reserva':   reserva['estado_reserva']
    }


def listar_reservas(fecha_especifica = None, usuario_especifico = None):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
       
        if fecha_especifica:
            cursor.execute("SELECT * FROM reservas WHERE DATE(fecha_reserva) = %s AND estado_reserva = 'pendiente'",(fecha_especifica,))
        
        elif usuario_especifico:
            cursor.execute("SELECT * FROM reservas WHERE id_usuario = %s AND estado_reserva = 'pendiente'", (usuario_especifico,))

        else:
            cursor.execute("SELECT * FROM reservas")
        
        reservas = cursor.fetchall()
        return [mensaje_reserva(reserva) for reserva in reservas]
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            



def crear_reserva(datos):
    id_usuario = datos['id_usuario']
    mesas = datos['mesas']
    fecha_reserva = datos['fecha_reserva'].strip()
    estado_reserva = datos.get('estado_reserva','pendiente')


    try:
        verificar_reservas_usuario(id_usuario)

    except ValueError:
        raise ValueError("Un usuario no puede tener más de 3 reservas pendientes simultaneamente.", 409)


    dat = datetime.strptime(fecha_reserva,FORMATO_FECHA)

    fecha_mysql = dat.strftime("%Y-%m-%d %H:%M:%S")



    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT 1 FROM usuarios WHERE id = %s", (id_usuario,))
        if not cursor.fetchone():
            raise ValueError("No existe ningun usuario con ese id",400)
        
        cursor.execute("INSERT INTO reservas (id_usuario, mesas, fecha_reserva, estado_reserva) VALUES (%s, %s, %s, %s)",
                       (id_usuario, mesas, fecha_mysql, estado_reserva))
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        id_reserva = cursor.fetchone()['id']
        return id_reserva

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def quitar_reserva(id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM reservas WHERE id = %s", (id,))

        if not cursor.fetchone():
            raise ValueError(f"No existe una reserva con id {id}", 404)

        cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
        conn.commit()

    finally:
        if cursor: 
            cursor.close()
        if conn: 
            conn.close()


def cambiar_estado_reserva(id,estado):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservas WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None, "La reserva no existe"
        cursor.execute("UPDATE reservas SET estado_reserva = %s WHERE id = %s",(estado, id,))
        conn.commit()
        return True,None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def verificar_reservas_usuario(id_usuario):
    reservas_usuario = listar_reservas(usuario_especifico=id_usuario)
    cantidad_reservas = len(reservas_usuario)

    if cantidad_reservas >= CANTIDAD_MAX_RESERVAS_USUARIO:
        raise ValueError
        