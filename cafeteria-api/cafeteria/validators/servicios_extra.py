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

    servicio_extra = cuerpo.get("servicio_extra")
    descripcion = cuerpo.get("descripcion")

    if servicio_extra is None or descripcion is None:
        return "Faltan campos por asignar",400

    if (not isinstance(servicio_extra,str)) or (not isinstance(descripcion,str)):
        return "El nombre del servicio_extra y su descripción deben ser de tipo string",400

    return None, None

def validar_body_patch_servicios_extra(cuerpo):

    if cuerpo is None:
        return "El body no cumple con el formato JSON",400

    tipos_datos_validos = {
        "servicio_extra": str,
        "descripcion": str,
    }

    for campo, valor in cuerpo.items(): #en vez de hacer campo.get, de cada campo, lo separo con un for
        
        #verifico que se respete la sintaxis del campo (su nombre) como el tipo de dato y su valor

        if campo not in tipos_datos_validos:
            return f"El campo {campo} no es válido", 400
        
        if not isinstance(valor, tipos_datos_validos[campo]): 
            return f"El campo {campo} debe ser de tipo {tipos_datos_validos[campo].__name__}", 400 #tipos_datos_validos[campo] por si solo devuelve <class 'int'>, con __name__ devuelve int a secas
       
    return None, None