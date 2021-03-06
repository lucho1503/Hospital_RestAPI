#!/usr/bin/python3
"""
Inicializa una instancia de Flask 
"""

from flask import Flask, make_response, jsonify
from models import storage
from models.base_model import BaseModel, Base
from api.v1.views import vistas
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.config['SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['SECURITY_PASSWORD_SALT'] = 'apis_por_doquier'
app.url_map.stric_slashes = False
app.register_blueprint(vistas)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
app.config.update(dict(
	DEBUG = True,
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS = True,
	MAIL_USE_SSL = False,
	MAIL_USERNAME = os.getenv('MAIL'),
	MAIL_DEFAULT_SENDER = os.getenv('MAIL'),
	MAIL_PASSWORD = os.getenv('PSWD_MAIL')
))

mail = Mail(app)

def usertoken(email):
	" Crea token para autenticarse por email"
	serializer = Serializer(app.config['SECRET_KEY'], salt=app.config['SECURITY_PASSWORD_SALT'])
	return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
	"verifica si el token es valido"
	serializer = Serializer(app.config['SECRET_KEY'])
	try:
		email = serializer.loads(
			token,
			salt=app.config['SECURITY_PASSWORD_SALT'],
			max_age=expiration
		)
	except:
		return False
	return email

@app.teardown_appcontext
def teardown_appcontext(self):
	"cierra la sesion"
	storage.close()


@app.errorhandler(404)
def not_found(error):
	"export json 404 error"
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	host = os.getenv('API_HOST', '0.0.0.0')
	port = os.getenv('API_PORT', 5000)
	app.run(host, port, threaded=True, debug=True)
