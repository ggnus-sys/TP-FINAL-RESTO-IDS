from flask import Blueprint, Flask, render_template, request, jsonify, abort, flash, redirect, url_for
from ..services.reviews import obtener_resenas, crear_resena, eliminar_resena
from ..utils import requiere_login, usuario_actual, token_actual

reviews_bp = Blueprint('reviews_bp', __name__)


@reviews_bp.route('/resenas', methods=['GET', 'POST'])
def get_resenas():
    if request.method == 'POST':
        if not usuario_actual():
            flash('Iniciá sesión para dejar una reseña.', 'error')
            return redirect(url_for('auth.login'))
        contenido = request.form.get("contenido")
        estrellas = request.form.get("estrellas")
        id_usuario = usuario_actual()['id']
        if estrellas:
            estrellas = int(estrellas)
        errores = []
        if not contenido:
            errores.append("El contenido de la reseña es obligatorio.")
        if not estrellas or estrellas < 1 or estrellas > 5:
            errores.append("Las estrellas deben ser un número entre 1 y 5.")
        if not id_usuario:
            errores.append("El ID del usuario es obligatorio.")
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('reviews_bp.get_resenas'))
        body = {
            "contenido": contenido,
            "estrellas": estrellas,
            "id_usuario": id_usuario
        }

        resultado = crear_resena(body, token_actual())
        if resultado:
            flash("Reseña creada con éxito.", 'success')
        else:
            flash("Error al crear reseña.", 'error')
        return redirect(url_for('reviews_bp.get_resenas'))
    # GET
    resenas = obtener_resenas()
    cantidad = len(resenas)
    if cantidad > 0:
        promedio = sum(r["estrellas"] for r in resenas) / cantidad
    else:
        promedio = 0
    return render_template(
        'reviews.html', resenas=resenas, usuario=usuario_actual(), promedio=promedio, cantidad=cantidad)


    
@reviews_bp.route('/resenas/<int:id>', methods=['GET'])
@requiere_login(rol='admin')
def delete_resena(id):
    resultado = eliminar_resena(id, token_actual())

    if resultado:
        flash("Reseña eliminada con exito.", 'success')
    else:
        flash('Error al eliminar reseña.' , 'error')
        
    return redirect(url_for('admin'))