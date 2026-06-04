from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.menu import obtener_menu, agregar_plato
from ..constants import CALIF_MIN, CALIF_MAX

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['GET'])
def detalle_menu():
    menu = obtener_menu()
    if not menu:
        abort(404, description=f'No se encontro el menu.')
    
    return render_template('menu.html', menu=menu)

@menu_bp.route('/adm', methods=['GET', 'POST'])
def admin_menu():
    if request.method == 'POST':
        # Aquí puedes manejar la lógica para agregar un nuevo plato al menú
        # Por ejemplo, podrías obtener los datos del formulario y luego redirigir a la página del menú
        plato = request.form.get('plato')
        precio = int(request.form.get('precio'))
        descripcion = request.form.get('descripcion')
        restricciones = request.form.get('restricciones_alimenticias')

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
