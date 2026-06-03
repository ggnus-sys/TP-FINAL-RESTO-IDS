from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..services.menu import obtener_menu
from ..constants import CALIF_MIN, CALIF_MAX

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/menu', methods=['GET'])
def detalle_menu():
    menu = obtener_menu()
    print(menu)
    if not menu:
        abort(404, description=f'No se encontro el menu.')
    
    return render_template('menu.html', menu=menu)