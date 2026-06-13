from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.menu import modificar_plato, obtener_menu, agregar_plato, borrar_plato, obtener_plato
from ..constants import CALIF_MIN, CALIF_MAX
from ..utils import requiere_login, usuario_actual

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['GET'])
def detalle_menu():
    menu = obtener_menu()
    if not menu:
        abort(404, description=f'No se encontro el menu.')
    
    return render_template('menu.html', menu=menu)

@menu_bp.route('/adm', methods=['GET', 'POST'])
@requiere_login(rol='admin')
def admin_menu():
    if request.method == 'POST':
        plato = request.form.get('plato')
        precio = int(request.form.get('precio'))
        descripcion = request.form.get('descripcion')
        restricciones = request.form.get('restricciones_alimenticias')
        plate_image = request.files['plate_image']
        plate_image.save(f'static/images/platos/plate_image_{plato}')

        errores = []
        if not plato:
            errores.append("El nombre del plato es obligatorio.")
        if not precio or precio <= 0:
            errores.append("Se debe introducir un precio válido y este tambien debe ser postitivo.")
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('menu.admin_menu'))

        resultado = agregar_plato(plato, precio, descripcion, restricciones)
        
        if resultado.get('ok'):
            flash('Plato agregado con exito.', 'success')
        else:
            for e in resultado.get('errores', ['Error al agregar el plato.']):
                flash(e, 'error')

        return redirect(url_for('menu.admin_menu'))

    menu = obtener_menu()
    if not menu:
        abort(404, description=f'No se encontro el menu.')

    return render_template('admin.html', menu=menu)

@menu_bp.route('/menu/delete/<int:plato_id>', methods=['GET'])
@requiere_login(rol='admin')
def delete_menu_item(plato_id):
    resultado = borrar_plato(plato_id)
    if resultado.get('ok'):
        flash('Plato eliminado con éxito.', 'success')
    else:
        for e in resultado.get('errores', ['Error al eliminar el plato.']):
                flash(e, 'error')

    return redirect(url_for('menu.admin_menu'))

@menu_bp.route('/menu/edit/<int:plato_id>', methods=['GET', 'POST'])
@requiere_login(rol='admin')
def editar_plato(plato_id):
    if request.method == 'GET':
        plato = obtener_plato(plato_id)
        if not plato:
            abort(404, description=f'No se encontro el plato con ID {plato_id}.')
        return render_template('editForm.html', plato=plato)

    if request.method == 'POST':
        plato_nombre = request.form.get('plato')
        precio = int(request.form.get('precio'))
        descripcion = request.form.get('descripcion')
        restricciones = request.form.get('restricciones_alimenticias')

        errores = []
        if not plato_nombre:
            errores.append("El nombre del plato es obligatorio.")
        if not precio or precio <= 0:
            errores.append("Se debe introducir un precio válido y este tambien debe ser postitivo.")
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('menu.editar_plato', plato_id=plato_id))

        resultado = modificar_plato(plato_id, plato_nombre, precio, descripcion, restricciones)

        if resultado.get('ok'):
            flash('Plato editado con exito.', 'success')
        else:
            for e in resultado.get('errores', ['Error al editar el plato.']):
                flash(e, 'error')

    return redirect(url_for('menu.admin_menu'))
    
