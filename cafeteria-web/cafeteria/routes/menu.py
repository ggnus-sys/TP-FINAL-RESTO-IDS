from flask import Flask,jsonify, render_template,request, Blueprint
#from ..services.menu import formato_mensaje_get, listar_platos ,modificar_plato ,crear_plato, eliminar_plato

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html')