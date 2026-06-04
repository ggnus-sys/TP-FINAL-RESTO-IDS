import os
import logging
from flask import Flask, render_template
from cafeteria.routes.reservas import reservas_bp
from cafeteria.routes.menu import menu_bp
from cafeteria.routes.reviews import reviews_bp
#from cafeteria.routes.usuarios import usuarios_bp


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.json.sort_keys = False

# Habilitar CORS para que el frontend pueda consumir la API

app.register_blueprint(reservas_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(reviews_bp)
#app.register_blueprint(usuarios_bp)
#app.register_blueprint(auth_bp) Si queremos hacer auth como en su ejemplo, tendremos que regisrar el blueprint

app.secret_key = os.urandom(24)  # Clave secreta para sesiones y flash messages

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port=5001)

