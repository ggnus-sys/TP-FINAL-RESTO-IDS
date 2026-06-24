from ..db import get_connection
from..constants import FORMATO_FECHA, CANTIDAD_MAX_RESERVAS_USUARIO, DURACION_TURNO, CAPACIDAD_MAX_WEB
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


def listar_reservas(fecha_especifica = None, usuario_especifico = None, estado = None):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
       
        query = "SELECT * FROM reservas WHERE 1=1"
        params = []

        if fecha_especifica:
            query += " AND DATE(fecha_reserva) = %s"
            params.append(fecha_especifica)
        
        if usuario_especifico:
            query += " AND id_usuario = %s"
            params.append(usuario_especifico)

        if estado:
            query += " AND estado_reserva = %s"
            params.append(estado)
        
        cursor.execute(query, tuple(params))
        
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
    fecha_datetime = datetime.strptime(fecha_reserva,FORMATO_FECHA)

    try:
        verificar_reservas_usuario(id_usuario)
        verificar_disponibilidad(fecha_datetime, mesas)


    except ValueError as e:
        raise ValueError(e.args[0], e.args[1])


    fecha_mysql = fecha_datetime.strftime("%Y-%m-%d %H:%M:%S")



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
    reservas_usuario = listar_reservas(usuario_especifico=id_usuario, estado='pendiente')
    cantidad_reservas = len(reservas_usuario)

    if cantidad_reservas >= CANTIDAD_MAX_RESERVAS_USUARIO:
        raise ValueError(f"Un usuario no puede tener más de 3 reservas pendientes simultaneamente.", 409)


def obtener_mesas_ocupadas_franja(fecha_str):

    nueva_reserva_inicio = fecha_str
    
    nueva_reserva_fin = nueva_reserva_inicio + DURACION_TURNO
    
    fecha_dia = nueva_reserva_inicio.strftime("%Y-%m-%d")
    
    reservas_pendientes = listar_reservas(fecha_especifica=fecha_dia,estado='pendiente')
    reservas_confirmadas = listar_reservas(fecha_especifica=fecha_dia,estado='confirmada')
    reservas_totales = reservas_pendientes + reservas_confirmadas
    
    mesas_ocupadas = 0

    if reservas_totales:
        for reserva in reservas_totales:
            reserva_inicio = reserva['fecha_reserva']
            reserva_fin = reserva_inicio + DURACION_TURNO
            
            if nueva_reserva_inicio < reserva_fin and nueva_reserva_fin > reserva_inicio:
                mesas_ocupadas += int(reserva['mesas'])
                
    return mesas_ocupadas


def verificar_disponibilidad(fecha_datetime, mesas):
    conflictos = []

    mesas_ocupadas = obtener_mesas_ocupadas_franja(fecha_datetime)

    if mesas_ocupadas + mesas > CAPACIDAD_MAX_WEB:
        mesas_libres = CAPACIDAD_MAX_WEB - mesas_ocupadas
        if mesas_libres <= 0:
            dia = fecha_datetime.strftime("%d/%m")
            hora = fecha_datetime.strftime("%H:%M")
            raise ValueError(f"Ya no quedan mesas disponibles para las {hora} del {dia}.", 409)
        else:
            raise ValueError(f"Solo quedan {mesas_libres} mesas disponibles para esa hora.", 409)