from flask import Blueprint, Flask, render_template, request, jsonify, abort, flash, redirect, url_for
from ..services.reviews import obtener_resenas, crear_resena, eliminar_resena

reviews_bp = Blueprint('reviews_bp', __name__)


@reviews_bp.route('/resenas', methods=['GET','POST'])
def get_resenas():
    if request.method == 'POST':

        #desgloso datos recibidos del formulario
        contenido = request.form.get("contenido")
        estrellas = int(request.form.get("estrellas"))
        id_usuario = int(request.form.get("id_usuario"))

        # validar los datos individualmente
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
        
        #acá se llega si no hay errores
        body = { "contenido": contenido,"estrellas": estrellas,"id_usuario": id_usuario}
        resultado = crear_resena(body)

        if resultado:
            flash("Reseña creada con exito.", 'success')
        else:
            flash('Error al crear reseña.' , 'error')
        
        return redirect(url_for('reviews_bp.get_resenas'))


    resenas = obtener_resenas()  # funcion para obtener las reseñas desde la base de datos

    if not resenas:
        abort(404, description="No se encontró ninguna reseña")
    
    return render_template('reviews.html', resenas=resenas)


    
    @reviews_bp.route('/resenas/<int:id>', methods=['DELETE'])
    def delete_resena(id):
        resultado = eliminar_resena(id)

        if resultado:
            flash("Reseña eliminada con exito.", 'success')
        else:
            flash('Error al eliminar reseña.' , 'error')
        
        return redirect(url_for('reviews_bp.get_resenas'))