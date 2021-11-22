#!/usr/bin/python3
"""
sistema despues de acceder
"""

from api.v1.app import usertoken, confirm_token, app
from flask_mail import Message
from api.v1.views import vistas
from flask import jsonify, abort, request, send_from_directory
from models import storage
from models.medico import Medico
from models.hospital import Hospital
from models.paciente import Paciente
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import datetime
import os

@vistas.route('/change_password', methods=['POST'])
@jwt_required
def change_password():
	""" 
	permite cambiar el password
	"""
	content = request.get_json()
	if content is None:
		abort(400, "Not es JSON")

	current_user = get_jwt_identity()
	old = content.get('old_password')
	new = content.get('new_password')
	usuario = storage.getbyid(current_user)
	autorizado = usuario.check_password(old)
	if not autorizado:
		return {"Error": "password invalido"}, 401

	usuario.password = new
	usuario.hash_password()
	if usuario.__class__.__name__ == 'Medico':
		usuario.activo = True
	usuario.save()

	return {"status": "ok"}, 200

@vistas.route('/reset_password', methods=['POST'])
def reset_password():
	"""
	permite reiniciar el password
	"""
	content = request.get_json()
	if content is None:
		abort(400, "Not es un JSON")

	usuario = storage.getbymail(content.get('correo'))
	acces_token = str(usertoken(hospital.correo))
	mail = 'http://0.0.0.0:5000/api/v1/reset/' + acces_token
	return {"status": mail}

@vistas.route('/reset', methods=['GET', 'PUT'])
def reset():
	if request.method == 'GET':
		try:
			email = confirm_token(token)
			return jsonify({"status": "ok"})
		except:
			return jsonify({"Error": "link no valido"}), 401

	if request.method == 'POST':
		try:
			email = confirm_token(token)
		except:
			pass
		usuario = storage.getbymail(mail)
		content = request.get_json()
		if content is None:
			abort(400, 'Not is a JSON')

		try:
			usuario.password = content.get("new_password")
			usuario.hash_password()
			usuario.save()
			return jsonify({"status": "ok"})
		except:
			return jsonify({"error": "link invalid"}), 401

@vistas.route('/servicios', methods=['GET'])
def return_services():
	servicios = storage.queryservicios()
	final = []
	for servicio in servicios:
		final.append(servicio.servicio)

	return jsonify(final), 201

@vistas.route('/registrar_medico', methods=['PUT'])
@jwt_required
def registrar_medico():
	"""
	permite a un hospital registrar un medico 
	"""
	content = request.get_json()
	if content is None:
		abort(400, 'NOT is a JSON')

	usuario = get_jwt_identity()
	autorizacion = storage.es_hospital(usuario)
	if not autorizacion:
		return jsonify({"Error": "usuario no autorizado"}), 401
	formulario = content.get('formulario')
	if len(formulario.get("especialidad")) < 1:
		return jsonify({"Error": "debe indicar la especialidad"}), 401

	medico = Medico(**content['formulario'])
	medico.hospital_id = usuario
	medico.hash_password()
	storage.agregar(medico)
	storage.save()
	return jsonify({"status": "CREATED"}), 201

@vistas.route('/registrar_observacion', methods=['POST'])
@jwt_required
def registrar_observacion():
	"""
	permite a un medico registrar la observacion 
	de un paciente
	"""
	content = request.get_json()
	if content is None:
		abort(400, "NOT is a JSON")

	usuario = get_jwt_identity()
	autorizacion = storage.es_medico(usuario)

	#if not autorizacion:
	#	return jsonify({"Error": "usuario no autorizado lok"}), 401

	formulario = content.get('formulario')
	medico = storage.getbyid(usuario)

	if medico.activo:
		medico.registrar_observacion(formulario)
		return jsonify({"status": "observacion registrada"}), 201
	else:
		return jsonify({"Error": "usuario no activo"}), 401

@vistas.route('/consultar', methods=['GET'])
@jwt_required
def consultar_observaciones():
	"""
	permite consultar observaciones a usuarios 
	registrados
	"""
	observaciones = {}
	id_usuario = get_jwt_identity()
	usuario = storage.getbyid(id_usuario)
	if usuario.activo:
		observaciones = usuario.registro()
	else:
		return jsonify({"Error": "usuario no autorizado"}), 401
	if len(observaciones) > 0:
		return jsonify(observaciones), 201
	else:
		return jsonify({"Error": "no hay registros guardados"}), 201

@vistas.route('/descargar_consulta', methods=['POST'])
@jwt_required
def descargar():
	""" 
	permite a un medico descargar
	registros de un paciente,
	retorna el link de descarga
	"""
	content = request.get_json()
	if content is None:
		abort(400, "Not is a JSON")

	paciente_id = content.get('paciente_id')
	usuario = get_jwt_identity()
	autorizacion = storage.es_medico(usuario)
	if not autorizacion:
		return jsonify({"Error": "usuario no autorizado"}), 401

	medico = storage.getbyid(usuario)
	if medico.activo:
		filename = medico.descargar_registro(paciente_id)
		acces_token = str(usertoken(filename))
		link = 'http://0.0.0.0:5000/api/v1/descargar/' + str(acces_token)
		return jsonify({"link": link})
	else:
		return jsonify({"Error": "usuario no autorizado"}), 401

@vistas.route('/descargar/<token>')
def get_csv(token):
	""" 
	retorna el archivo .csv
	desde el directorio root
	"""
	try:
		filename = str(acces_token(token))
	except:
		abort(400)
	try:
		return send_from_directory(os.getcwd(),
									filename=filename,
									as_attachment=True)
	except FileNotFoundError:
		abort(400)