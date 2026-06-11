import logging
from flask import Flask
from flask_cors import CORS
from cafeteria.constants import BASE_URL
from cafeteria.routes.reservas import reservas_bp
from cafeteria.routes.menu import menu_bp
from cafeteria.routes.reviews import reviews_bp
from cafeteria.routes.usuarios import usuarios_bp
from cafeteria.routes.auth import auth_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# Habilitar CORS para que el frontend pueda consumir la API
CORS(app)

app.register_blueprint(reservas_bp, url_prefix=BASE_URL)
app.register_blueprint(menu_bp, url_prefix=BASE_URL)
app.register_blueprint(reviews_bp, url_prefix=BASE_URL)
app.register_blueprint(usuarios_bp, url_prefix=BASE_URL)
app.register_blueprint(auth_bp, url_prefix=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port=5000)

