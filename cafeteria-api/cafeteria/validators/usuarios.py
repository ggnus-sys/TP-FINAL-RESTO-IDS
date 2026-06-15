from ..constants import EMAIL_REGEX, ROLES_VALIDOS

#validación del tp anterior, devuelve (None, None) si anda todo bien. Si no, (mensaje, error)
def validar_body_usuario(body):
    if body is None:
        return "El body debe ser un JSON válido", 404
    
    nombre = body.get("nombre")
    apellido = body.get("apellido")
    email = body.get("email")
    password = body.get("password")
    rol = body.get("rol", "cliente")

    if not nombre or not apellido or not email or not password:
        return "Hacen falta campos obligatorios", 400
    
    for campo, valor in [("nombre", nombre), ("apellido", apellido), ("email", email), ("password", password)]:
        if not isinstance(valor, str) or not valor.strip():
            return f"El campo '{campo}' debe ser una cadena no vacía", 400
        
    if not EMAIL_REGEX.match(email):
        return "El email no es valido",400
    
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres", 400
    
    if rol not in ROLES_VALIDOS:
        return "El rol no es válido", 400
    
    return None, None


#tuve que agregar esta funcion para que reciba solo mail y password para el login
def validar_body_login(body):
    if body is None:
        return "El body debe ser un JSON válido", 404
    
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return "Hacen falta campos obligatorios", 400
    
    for campo, valor in [("email", email), ("password", password)]:
        if not isinstance(valor, str) or not valor.strip():
            return f"El campo '{campo}' debe ser una cadena no vacía", 400
        
    if not EMAIL_REGEX.match(email):
        return "El email no es valido",400
    
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres", 400
    
    return None, None