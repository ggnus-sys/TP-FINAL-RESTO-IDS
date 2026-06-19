from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.servicios_extra import modificar_servicio_extra, obtener_servicios_extra, agregar_servicio_extra, borrar_servicio_extra, obtener_servicio_extra
from ..constants import CALIF_MIN, CALIF_MAX
from ..utils import requiere_login, token_actual

servicios_extra_bp = Blueprint('servicios-extra', __name__)

@servicios_extra_bp.route('/servicios-extra', methods=['GET'])
def detalle_servicios_extra():
    servicios_extra = obtener_servicios_extra()
    if not servicios_extra:
        abort(404, description=f'No se encontro el servicios_extra.')
    
    return render_template('servicios-extra.html', servicios_extra=servicios_extra)

@servicios_extra_bp.route('/servicios-extra/agregar-servicio', methods=['GET', 'POST'])
@requiere_login(rol='admin')
def admin_servicios_extra():
    if request.method == 'POST':
        nombre_servicio = request.form.get('nombre_servicio')
        descripcion = request.form.get('descripcion')
        service_image = request.files['service_image']
        service_image.save(f'static/images/servicios-extra/service_image_{nombre_servicio}')

        errores = []
        if not nombre_servicio:
            errores.append("El nombre del servicio extra es obligatorio.")
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('servicios-extra.admin_servicios_extra'))

        resultado = agregar_servicio_extra(nombre_servicio, descripcion, token_actual())
        
        if resultado.get('ok'):
            flash('servicio extra agregado con exito.', 'success')
        else:
            for e in resultado.get('errores', ['Error al agregar el servicio_extra.']):
                flash(e, 'error')

        return redirect(url_for('servicios-extra.admin_servicios_extra'))

    

    return redirect(url_for('admin'))

@servicios_extra_bp.route('/servicios-extra/delete/<int:servicio_extra_id>', methods=['GET'])
def delete_servicio_extra(servicio_extra_id):
    resultado = borrar_servicio_extra(servicio_extra_id)
    if resultado.get('ok'):
        flash('servicio extra eliminado con éxito.', 'success')
    else:
        for e in resultado.get('errores', ['Error al eliminar el servicio extra.']):
                flash(e, 'error')

    return redirect(url_for('servicios-extra.admin_servicios_extra'))

@servicios_extra_bp.route('/servicios-extra/edit/<int:servicio_extra_id>', methods=['GET', 'POST'])
def editar_servicio_extra(servicio_extra_id):
    if request.method == 'GET':
        servicio_extra = obtener_servicio_extra(servicio_extra_id)
        if not servicio_extra:
            abort(404, description=f'No se encontro el servicio extra con ID {servicio_extra_id}.')
        return render_template('editForm-servicios-extra.html', servicio=servicio_extra)

    if request.method == 'POST':
        nombre_servicio = request.form.get('nombre_servicio')
        descripcion = request.form.get('descripcion')
        service_image = request.files['service_image']
        if service_image.filename != '':
            service_image.save(f'static/images/servicios-extra/service_image_{nombre_servicio}')

        errores = []
        if not nombre_servicio:
            errores.append("El nombre del servicio extra es obligatorio.")
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('servicios-extra.editar_servicio_extra', servicio_extra_id=servicio_extra_id))

        resultado = modificar_servicio_extra(servicio_extra_id, nombre_servicio, descripcion)

        if resultado.get('ok'):
            flash('servicio extra editado con exito.', 'success')
        else:
            for e in resultado.get('errores', ['Error al editar el servicio extra.']):
                flash(e, 'error')

    return redirect(url_for('servicios-extra.admin_servicios_extra'))
    
