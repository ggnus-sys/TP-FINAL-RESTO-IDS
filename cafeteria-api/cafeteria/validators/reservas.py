from datetime import date, datetime
from ..constants import FORMATO_FECHA, ESTADOS_VALIDOS

def validar_body_reserva(body):
    if body is None:
        return "El body debe ser un JSON válido", 400
    
    id_usuario = body.get("id_usuario")
    mesas = body.get("mesas")
    fecha_reserva = body.get("fecha_reserva")
    estado_reserva = body.get("estado_reserva", "pendiente").strip()


    if id_usuario is None or mesas is None or fecha_reserva is None or estado_reserva is None:
        return "Hacen falta campos obligatorios", 400

    try:
        fecha_reserva = datetime.strptime(fecha_reserva,FORMATO_FECHA).date()

    except ValueError:
        return "Formato de fecha inválido (ejemplo de fecha correcta: '2026-08-18')", 400
    

    if not isinstance(id_usuario, int) or not isinstance(mesas, int) or not isinstance(fecha_reserva, date) or not isinstance(estado_reserva, str):
        return f"El id del usuario y la cantidad de mesas deben ser numeros enteros, la fecha de reserva una fecha con formato YYYY-MM-DD y el estado de la reserva un string", 400
        
    if mesas < 1 or mesas > 30:
        return "La cantidad de mesas es invalida",400

    if estado_reserva not in ESTADOS_VALIDOS:
        return "Estado de reserva inválido",400


    return None, None