def validar_body_resena_post(cuerpo):
    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    contenido = cuerpo.get("contenido")
    estrellas = cuerpo.get("estrellas")
    id_usuario = cuerpo.get("id_usuario")

    if contenido is None or estrellas is None or id_usuario is None:
        return "Faltan campos por asignar", 400

    if not isinstance(contenido, str):
        return "El contenido debe ser de tipo string", 400
    
    if not isinstance(estrellas, int) or estrellas not in range(1, 6):
        return "Las estrellas deben ser un número entero entre 1 y 5", 400
    
    if not isinstance(id_usuario, int) or id_usuario <= 0:
        return "El id_usuario debe ser un número entero positivo", 400

    return None, None


def validar_body_resena_patch(cuerpo):
    if cuerpo is None:
        return "El body no cumple con el formato JSON", 400

    if "contenido" in cuerpo and not isinstance(cuerpo["contenido"], str):
        return "El contenido debe ser de tipo string", 400

    if "estrellas" in cuerpo:
        if not isinstance(cuerpo["estrellas"], int) or cuerpo["estrellas"] not in range(1, 6):
            return "Las estrellas deben ser un número entero entre 1 y 5", 400

    return None, None
