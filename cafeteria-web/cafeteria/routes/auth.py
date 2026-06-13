from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.auth import login_api, register_api
from ..utils import guardar_sesion, limpiar_sesion, usuario_actual

auth_bp = Blueprint('auth', __name__)

#login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Completá todos los campos.', 'error')
            
            return redirect(url_for('auth.login'))
        
        resultado = login_api(email, password)

        if resultado.get('ok'):
            guardar_sesion(resultado['token'], resultado['usuario'])
            flash('Bienvenido de nuevo !', 'success')
            return redirect(url_for('index'))
        else:
            for error in resultado.get('errores', []):
                flash(error, 'error')

    
    return render_template('login.html')



#register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')

        errores = []

        if not email:
            errores.append('El email es obligatorio.')

        if not password:
            errores.append('La contraseña es obligatoria.')

        if not nombre:
            errores.append('El nombre es obligatorio.')

        if not apellido:
            errores.append('El apellido es obligatorio.')

        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('auth.register'))

        resultado = register_api(nombre, apellido, email, password)

        if resultado.get('ok'):
            flash('Usuario registrado con éxito. Iniciá sesión para continuar.', 'success')
            return redirect(url_for('auth.login'))
        else:
            for error in resultado.get('errores', []):
                flash(error, 'error')

    return render_template('register.html')


#logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    limpiar_sesion()

    flash('Sesión cerrada exitosamente.', 'success')
    
    return redirect(url_for('index'))