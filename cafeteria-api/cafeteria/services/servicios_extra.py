from ..db import get_connection

def formato_mensaje_get(servicio_extra):
    return {
        'id': servicio_extra['id'],
        'nombre_servicio': servicio_extra['nombre_servicio'],
        'descripcion': servicio_extra['descripcion'],
    }

def listar_servicios_extra(id_servicio_extra, nombre_servicio_extra):

    query = "SELECT * FROM servicios_extra"
    filtros = []
    params = []

    if id_servicio_extra:
        filtros.append("id = %s")
        params.append(id_servicio_extra)
    if nombre_servicio_extra:
        filtros.append("nombre_servicio LIKE %s") 
        params.append(f"%{nombre_servicio_extra}%") # por ejemplo %pizza% → significa contiene "pizza" sintaxis SQL (busca los nombres que contengan pizza)
    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        servicios_extra = cursor.fetchall()
        return [formato_mensaje_get(servicio) for servicio in servicios_extra] #a cada servicio_extra obtenido del fetchall, formatealo
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def modificar_servicio_extra(id,cuerpo):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

        cursor.execute("SELECT id FROM servicios_extra WHERE id = %s", (id, ))
        
        if not cursor.fetchone():
            raise ValueError(f"El servicio_extra cuyo ID es: {id} no existe en la base de datos.",404)
        
        campos = []
        valores = []

        for campo, valor in cuerpo.items():
            campos.append(f"{campo} = %s")
            valores.append(valor)
            
        valores.append(id)
                        
        query = "UPDATE servicios_extra SET " + ",".join(campos) + " WHERE id = %s"
        
        cursor.execute(query, valores)
        conn.commit()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def crear_servicio_extra(datos):

    conn = None
    cursor = None

    nombre_servicio = datos["nombre_servicio"].strip()
    descripcion = datos["descripcion"].strip()
        
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)
        
        cursor.execute("SELECT id FROM servicios_extra WHERE nombre_servicio = %s", (nombre_servicio,))

        if cursor.fetchone():
            raise ValueError(f"ya existe un servicio_extra con el nombre {nombre_servicio}", 409)
        
        cursor.execute("INSERT INTO servicios_extra (nombre_servicio, descripcion) VALUES (%s,%s)", (nombre_servicio, descripcion))
        conn.commit()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def eliminar_servicio_extra(id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

        cursor.execute("SELECT id FROM servicios_extra WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise ValueError(f"No existe un servicio_extra con id {id}", 404)

        cursor.execute("DELETE FROM servicios_extra WHERE id = %s", (id,))
        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
