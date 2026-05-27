def validar_body_menu(cuerpo):

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

    return None, None