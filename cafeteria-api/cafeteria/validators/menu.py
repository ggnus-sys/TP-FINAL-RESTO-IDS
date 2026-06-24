def validar_params_get_menu(id_base, restricciones):
    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']
    
    id_plato = None
    if id_base is not None:
        try:
            id_plato = int(id_base) #lo convierto a entero para ver si es <= 0
        except ValueError:
            return None, "El id debe ser un entero.", 400
        if id_plato <= 0:
            return None, "El id debe ser un entero positivo.", 400

    for restriccion in restricciones:
        if restriccion not in RESTRICCIONES_VALIDAS:
            return None, f"La restricción '{restriccion}' no es válida.", 400

    return id_plato, None, None 

def validar_body_post_menu(cuerpo):

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    plato = cuerpo.get("plato")
    precio = cuerpo.get("precio")
    descripcion = cuerpo.get("descripcion")
    restriccion = cuerpo.get("restricciones_alimenticias")

    if plato is None or precio is None or descripcion is None or restriccion is None:
        return "Faltan campos por asignar",400
    
    if (not isinstance(plato,str)) or (not isinstance(precio,int)) or (precio <= 0) or (not isinstance(descripcion,str) or (not isinstance(restriccion,str))):
        return "El nombre del plato, su descripción y la restricción alimenticia (si abarca alguna) deben ser de tipo string. El precio debe ser de tipo integer y mayor a 0",400

    restriccion_limpia = restriccion.replace(" ", "")
    if restriccion_limpia != "":
        restricciones_ingresadas = restriccion_limpia.split(",")
        for r in restricciones_ingresadas:
            if r not in RESTRICCIONES_VALIDAS:
                return f"La restricción '{r}' no es válida.", 400

    return None, None

def validar_body_patch_menu(cuerpo):

    RESTRICCIONES_VALIDAS = ['vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten']

    if cuerpo is None:
        return "El body no cumple con el formato JSON",400

    plato = cuerpo.get("plato")
    precio = cuerpo.get("precio")
    descripcion = cuerpo.get("descripcion")
    restriccion = cuerpo.get("restricciones_alimenticias")

    if plato is None or precio is None or descripcion is None or restriccion is None:
        return "Faltan campos por asignar",400
    
    if (not isinstance(plato,str)) or (not isinstance(precio,int)) or (precio <= 0) or (not isinstance(descripcion,str) or (not isinstance(restriccion,str))):
        return "El nombre del plato, su descripción y la restricción alimenticia (si abarca alguna) deben ser de tipo string. El precio debe ser de tipo integer y mayor a 0",400

    restriccion_limpia = restriccion.replace(" ", "")
    if restriccion_limpia != "":
        restricciones_ingresadas = restriccion_limpia.split(",")
        for r in restricciones_ingresadas:
            if r not in RESTRICCIONES_VALIDAS:
                return f"La restricción '{r}' no es válida.", 400
    
       
    return None, None