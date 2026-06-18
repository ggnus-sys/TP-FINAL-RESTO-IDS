from datetime import date, datetime
from ..utils import validar_entero, validar_fecha_futura, validar_formato_fecha, validar_maximo, validar_minimo, validar_set, validar_string_no_vacio
from ..constants import FORMATO_FECHA, ESTADOS_VALIDOS

def validar_body_reserva(body):
    if body is None:
        return "El body debe ser un JSON válido", 400
    
    id_usuario = body.get("id_usuario")
    mesas = body.get("mesas")
    fecha_reserva = body.get("fecha_reserva")
    estado_reserva = body.get("estado_reserva", "pendiente").strip()

    try:
        validar_string_no_vacio(estado_reserva, "estado_reserva")
        validar_string_no_vacio(mesas, "mesas")
        validar_string_no_vacio(fecha_reserva, "fecha_reserva")

        fecha_reserva = validar_formato_fecha(fecha_reserva, FORMATO_FECHA, "fecha_reserva")
        
        validar_fecha_futura(fecha_reserva)

        validar_entero(id_usuario, "id_usuario")
        validar_entero(mesas, "mesas")

        validar_minimo(mesas, 1, "mesas")    
        validar_maximo(mesas, 2, "mesas")

        validar_set(estado_reserva, ESTADOS_VALIDOS, "estado_reserva")
    except ValueError as e:
        return str(e), 400

    return None, None

def validar_body_estado(body):
    if body is None:
        return "El body debe ser un JSON valido", 400
    estado = body.get("estado")
    try:
        validar_string_no_vacio(estado, "estado")
        validar_set(estado, ESTADOS_VALIDOS, "estado")
    except ValueError as e:
        return str(e), 400
    return None, None