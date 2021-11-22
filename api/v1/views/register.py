#!usr/bin/python3
"""
clases encargadas de registrar y confirmar usuario.
"""

from api.v1.app import usertoken, confirm_token, mail
from api.v1.views import vistas
from flask_mail import Message
from flask import jsonify, abort, request
from models import storage
from models.hospital import Hospital
from models.paciente import Paciente
from models.medico import Medico

@vistas.route('/registrar', methods=['POST'])
def sign_up():
	""" 
	crea una instancia de un usuario 
	dependiendo de su tipo y la almacena en
	base de datos
	"""
	content = request.get_json()
	if content is None:
		abort(400, 'No es un Json')
	usuario = content.get('usuario')
	usuario_id = content.get('formulario').get('id')
	if not storage.verificar_id(usuario_id):
		return jsonify({"Error": "id inavliado"}), 401
	correo = content.get('formulario').get('correo')
	msg = Message(recipients=[correo])
	if not storage.verificar_correo(correo):
		return jsonify({"Eroor": "correo invalido"}), 401
	servicios = content.get("servicios")
	if usuario == 'hospital':
		if len(servicios) < 1:
			return jsonify({"Errorr": "debe registrar servicios"}), 401
		hospital = Hospital(**content['formulario'])
		hospital.hash_password()
		storage.agregar(hospital)
		storage.save()
		mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
		user = str(usertoken(hospital.correo))
		mail_confirm = mail_confirm + user			

	elif usuario == 'paciente':
		if len(content.get('formulario').get('fecha_nacimiento')) < 1:
			return jsonify({"Erorr": "debe poner la fecha de nacimniento"}), 401
		paciente = Paciente(**content['formulario'])
		paciente.hash_password()
		storage.agregar(paciente)
		storage.save()
		mail_confirm = 'http://0.0.0.0:5000/api/v1/confirmar/'
		user = str(usertoken(paciente.correo))
		mail_confirm = mail_confirm + user

	else:
		return jsonify({"Errorr": "usuario incorrecto"}), 400

	texto_msn = "<p> Gracias por registrarte </p> <br>"
	texto_msn += '<a href="'+mail_confirm+'"> confirma tu registro.</a><br>'
	msg.subject = "confirmar registro"
	msg.html = texto_msn
	mail.send(msg)
	return jsonify({"Status": "ok"}), 201

@vistas.route('/confirmar/<token>')
def confirmar(token):
	"""
	verifica un regsitro por email 
	"""
	try:
		email = confirm_token(token)
	except:
		pass
	usuario = storage.getbymail(email)
	print(email)
	usuario.activo = True
	usuario.save()
	return jsonify({"status": "ok"})