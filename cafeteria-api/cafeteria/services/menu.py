from ..db import get_connection

def formato_mensaje_get(plato):
    restricciones = plato['restricciones_alimenticias']
    if isinstance(restricciones, set): #como restricciones_alimenticias es tipo dato set, lo convertimos a un string con elemntos unidos por "," para que pueda se le pueda aplicar jsonify
        restricciones = ",".join(restricciones)
    return {
        'id': plato['id'],
        'plato': plato['plato'],
        'precio': plato['precio'],
        'descripcion': plato['descripcion'],
        'restricciones_alimenticias': restricciones
    }

def listar_platos(id_plato, nombre_plato, restricciones):

    query = "SELECT * FROM menu"
    filtros = []
    params = []

    if id_plato:
        filtros.append("id = %s")
        params.append(id_plato)
    if nombre_plato:
        filtros.append("plato LIKE %s") 
        params.append(f"%{nombre_plato}%") # por ejemplo %pizza% → significa contiene "pizza" sintaxis SQL (busca los nombres que contengan pizza)
    for restriccion in restricciones:
        filtros.append("FIND_IN_SET(%s, restricciones_alimenticias)") #busca que el valor dado se encuentre dentro de los permitidos por el SET definido en la tabla
        params.append(restriccion)
    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        platos = cursor.fetchall()
        return [formato_mensaje_get(plato) for plato in platos] #a cada plato obtenido del fetchall, formatealo
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def modificar_plato(id,cuerpo):

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

        cursor.execute("SELECT id FROM menu WHERE id = %s", (id, ))
        
        if not cursor.fetchone():
            raise ValueError(f"El plato cuyo ID es: {id} no existe en la base de datos.",404)
        
        campos = []
        valores = []

        for campo, valor in cuerpo.items():

            if campo == "restricciones_alimenticias":
                valor = valor.replace(" ", "") #para que al hacer append, quede un string con elementos separados por comas, sin espacios
                    
            campos.append(f"{campo} = %s")
            valores.append(valor)
            
        valores.append(id)
                        
        query = "UPDATE menu SET " + ",".join(campos) + " WHERE id = %s"
        
        cursor.execute(query, valores)
        conn.commit()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def crear_plato(datos):

    conn = None
    cursor = None

    plato = datos["plato"].strip()
    precio = datos["precio"]
    descripcion = datos["descripcion"].strip()
    restriccion = datos["restricciones_alimenticias"].replace(" ", "") #deja el set como estaba, solo elimina los espacios que haya entre las comas y los elementos
        
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)
        
        cursor.execute("SELECT id FROM menu WHERE plato = %s", (plato,))

        if cursor.fetchone():
            raise ValueError(f"ya existe un plato con el nombre {plato}", 409)
        
        cursor.execute("INSERT INTO menu (plato, precio, descripcion, restricciones_alimenticias) VALUES (%s,%s,%s,%s)", (plato, precio, descripcion, restriccion))
        conn.commit()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def eliminar_plato(id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)

        cursor.execute("SELECT id FROM menu WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise ValueError(f"No existe un usuario con id {id}", 404)

        cursor.execute("DELETE FROM menu WHERE id = %s", (id,))
        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
