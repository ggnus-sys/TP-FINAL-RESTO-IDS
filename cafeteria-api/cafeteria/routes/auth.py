from flask import Blueprint, jsonify, request
from ..services.auth import registrar_usuario, login_usuario


auth_bp = Blueprint('auth_bp', __name__)


#TODO:grandisima funcion de leo, en el trello me voy a poner para hacer algo parecido en usuarios y dejarlo más limpito

# ------------------- wrapper manejo errores-----------------------------
def _ejecutar(funcion, status_ok=200):
    """Wrapper que toma el body JSON, invoca la funcion del service y maneja errores."""
    body = request.get_json(silent=True)

    try:
        resultado = funcion(body)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400

        return jsonify(e.args[0]), status

    return jsonify(resultado), status_ok


# ------------- registro POST --------------

@auth_bp.route('/register', methods=['POST'])
def post_register():
    return _ejecutar(registrar_usuario, status_ok=201)


# -----------login POST --------------

@auth_bp.route('/login', methods=['POST'])
def post_login():
    return _ejecutar(login_usuario, status_ok=200)