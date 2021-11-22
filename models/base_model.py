#!/usr/bin/python3
"""
clase base con todos los atributos principales
"""

import models
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

" Base declarativa para sqlalchemy"

Base = declarative_base()

class BaseModel:
	"""
	atributos y funciones pricipales
	"""
	id = Column(String(60), primary_key=True)
	correo = Column(String(60), unique=True)
	telefono = Column(String(60))
	password = Column(String(60))
	nombre = Column(String(60))
	direccion = Column(String(60))
	activo = Column(Boolean, unique=False, default=False)

	def __init__(self, *args, **kwargs):
		"""
		inicializa las instancias de la clase apartir 
		de un diccionario 
		"""
		if kwargs:
			for key, value in kwargs.items():
				if key != '__class__' and key != "activo":
					setattr(self, key, value)

		else:
			pass

	def hash_password(self):
		"""
		genera un password encriptado
		"""
		self.password = generate_password_hash(self.password).decode('utf8')

	def check_password(self, password):
		""" verifica si el password es correco 
		apartir de un hash
		"""
		return check_password_hash(self.password, password)

	def save(self):
		"""
		guarda el objeto en la base datos 
		"""
		models.storage.agregar(self)
		models.storage.save()