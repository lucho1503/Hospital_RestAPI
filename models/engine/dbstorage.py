#!/usr/bin/python3
"""
clase encargada de gestionar todos
los elementos de la base de datos
"""

import sqlalchemy as db
from sqlalchemy import Table, MetaData, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base, BaseModel
from models.hospital import Hospital
from models.servicios import Servicio
from models.medico import Medico
from models.observaciones import Observacion
from models.paciente import Paciente


class Database:
	""" Interactua con la base de datos """

	__engine = None
	__session = None

	def __init__(self):
		""" inicializa la base de datos """
		self.__engine = db.create_engine('postgresql://postgres:root@localhost/hospital')
		print("DB instance created")

	def agregar(self, obj):
		""" agrega el objeto a la base de datos """
		self.__session.add(obj)

	def agregar_servicios(self, servicios, hospital):
		"""
		agregar servicios a la base de datos
		"""
		lista_agregados = []
		servicios_actuales = self.queryservicios()
		for servicio in servicios_actuales:
			if servicio.servicio in servicios:
				hospital.servicios.append(servicio)
				lista_agregados.append(servicio.servicio)


		for servicio in servicios:
			if servicio in lista_agregados:
				pass
			else:
				new_servicio = Servicio(servicio=servicio)
				self.__session.add(servicio)
				hospital.servicios.append(new_servicio)

	def verificar_id(self, usuario_id):
		""" 
		verifica si el usuario ya existe
		"""
		if len(usuario_id) < 1 or not usuario_id:
			return False
		usuario = self.getbyid(usuario_id)
		if type(usuario) != dict:
			return False
		return True

	def verificar_correo(self, correo):
		"""
		verifica si el correo existe
		"""
		if len(correo) < 1 or not correo:
			return False
		correo = self.getbymail(correo)
		if type(correo) != dict:
			return False
		return True

	def query(self, query):
		"""
		trae las tablas y las convierte en objetos
		que son almacenados como valores en un 
		diccionario, este se devuelve al final con 
		las id de los objetos como claves
		"""
		objetos = {}
		queri = eval(query)
		for row in self.__session.query(queri).all():
			key = str(row.id)
			objetos[key] = row
		return objetos

	def queryservicios(self):
		"""
		devuelve una lista con todos los servicios
		"""
		return self.__session.query(Servicio).all()

	def querymail(self, mail):
		"""
		trae las tablas y las convierte en objetos
		que son almacenados como valores en un 
		diccionario, este es el que se devuelve con las
		id de los objetos como claves
		"""
		objetos = {}
		queri = eval(mail)
		for row in self.__session.qu ery(queri).all():
			key = str(row.correo)
			objetos[key] = row
		return objetos

	def query_registros(self):
		""" 
		retorna una lista con todos los 
		registros
		"""
		return self.__session.query(Observacion).all()

	def getbyid(self, id):
		"""
		devuelve un objeto a partir de su id
		"""
		objetos = {}
		for elem in ["Hospital", "Medico", "Paciente"]:
			objetos = self.query(elem)
			if id in objetos:
				return objetos[id]
		return objetos

	def getbymail(self, mail):
		"""
		devuelve un objeto a partir de su mail
		"""
		objetos = {}
		for elem in ["Hospital", "Medico", "Paciente"]:
			objetos = self.querymail(elem)
			if mail in objetos:
				return objetos[mail]
		return objetos

	def es_hospital(self, id):
		""" verifica si el usuario es paciente """
		user = self.getbyid(id)
		if "Hospital" in str(user.__class__):
			return True
		return False

	def es_medico(self, id):
		"""
		verifica si el objeto es de tipo medico
		"""
		usuario = self.getbyid(id)
		if "Medico" not in str(usuario.__class__):
			return False
		return True

	def save(self):
		""" confirma los cambios """
		self.__session.commit()

	def reload(self):
		""" carga los datos en la base de datos """
		Base.metadata.create_all(self.__engine)
		sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
		Session = scoped_session(sess_factory)
		self.__session = Session

	def close(self):
		""" cierra la sesion en la base de datos """
		self.__session.remove()