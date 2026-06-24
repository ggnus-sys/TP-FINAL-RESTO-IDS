def validar_id_get_servicios_extra(id_base):
    
    id_servicio_extra = None
    if id_base is not None:
        try:
            id_servicio_extra = int(id_base) #lo convierto a entero para ver si es <= 0
        except ValueError:
            return None, "El id debe ser un entero.", 400
        if id_servicio_extra <= 0:
            return None, "El id debe ser un entero positivo.", 400

    return id_servicio_extra, None, None 

def validar_body_post_servicios_extra(cuerpo):

    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    nombre_servicio = cuerpo.get("nombre_servicio")
    descripcion = cuerpo.get("descripcion")

    if nombre_servicio is None or descripcion is None:
        return "Faltan campos por asignar",400

    if (not isinstance(nombre_servicio,str)) or (not isinstance(descripcion,str)):
        return "El nombre del servicio extra y su descripción deben ser de tipo string",400

    return None, None

def validar_body_patch_servicios_extra(cuerpo):

    if cuerpo is None:
        return "El body no cumple con el formato JSON",400

    nombre_servicio = cuerpo.get("nombre_servicio")
    descripcion = cuerpo.get("descripcion")

    if nombre_servicio is None or descripcion is None:
        return "Faltan campos por asignar",400

    if (not isinstance(nombre_servicio,str)) or (not isinstance(descripcion,str)):
        return "El nombre del servicio extra y su descripción deben ser de tipo string",400

    return None, None