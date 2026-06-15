from ..db import get_connection

def listar_resenas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resenas")
        return cursor.fetchall()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def filtrar_resena(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resenas WHERE id = %s", (id,))
        return cursor.fetchone()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def crear_resena(datos):
    contenido = datos.get("contenido")
    estrellas = datos.get("estrellas")
    id_usuario = datos.get("id_usuario")
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            return None, "El usuario no existe"
        cursor.execute("INSERT INTO resenas (contenido, estrellas, id_usuario) VALUES (%s,%s,%s)",
                      (contenido, estrellas, id_usuario))
        conn.commit()
        return True, None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def eliminar_resena(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resenas WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None
        cursor.execute("DELETE FROM resenas WHERE id = %s", (id,))
        conn.commit()
        return True
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def actualizar_resena(id, datos):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resenas WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None
        campos = []
        valores = []
        if "contenido" in datos:
            campos.append("contenido = %s")
            valores.append(datos["contenido"])
        if "estrellas" in datos:
            campos.append("estrellas = %s")
            valores.append(datos["estrellas"])
        valores.append(id)
        cursor.execute(f"UPDATE resenas SET {', '.join(campos)} WHERE id = %s", valores)
        conn.commit()
        return True
    finally:
        if cursor: cursor.close()
        if conn: conn.close()