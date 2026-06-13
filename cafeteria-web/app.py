import os
import logging
from flask import Flask, render_template, send_file, request
from cafeteria.routes.reservas import reservas_bp
from cafeteria.routes.menu import menu_bp
from cafeteria.routes.reviews import reviews_bp
from cafeteria.routes.auth import auth_bp
from cafeteria.services.mailer import enviar_qr_confirmacion_reserva
from flask_mail import Mail
import segno

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.json.sort_keys = False

#configuracion para flask-mail(SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'kaifernoreply@gmail.com'
app.config['MAIL_PASSWORD'] = 'frls gjlo zfna gfjn'  # En un entorno real, esta contraseña no debería estar hardcodeada
app.config['MAIL_DEFAULT_SENDER'] = 'kaifernoreply@gmail.com'
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

app.register_blueprint(reservas_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)
#app.register_blueprint(usuarios_bp)
app.secret_key = os.getenv('SECRET_KEY', 'clave-kaifer') #cambié la clave anterior por una fija para que no se deslogueen los usuarios ya hechos cada vez que reiniciemos
#tengo entendido que tanto acá como JWT_SECRET (en la api), lo ideal es que la clave se obtenga del env
#con .getenv al no encontrar nada toma por default 'clave-kaifer' (mismo en en JWT_SECRET)
#aunque la buena práctica sería que no esté hardcodeada acá xd



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        mensaje=error.description
    ), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
