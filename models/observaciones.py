#!/usr/bin/python3
"""
clase observacion que hereda de Base
"""

import models
from models.base_model import Base
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

class Observacion(Base):
	"""
	metodos y atributos de clase observaion
	"""
	__tablename__ = 'observaciones'
	id = Column(String(60), primary_key=True)
	hospital = Column(String(60))
	medico = Column(String(60))
	especialidad = Column(String(60))
	registro = Column(String(60))
	hospital_id = Column(String(60), ForeignKey('hospitales.id'), nullable=False)
	medico_id = Column(String(60), ForeignKey('medicos.id'), nullable=False)
	paciente_id = Column(String(60), ForeignKey('pacientes.id'), nullable=False)

	def to_dict(self):
		"""
		devuelve un diccionario apartir de un objeto,
		con los atributos requeridos para consultar
		"""
		new_dict = {}
		new_dict['hospital'] = self.hospital
		new_dict['medico'] = self.medico
		new_dict['especialidad'] = self.especialidad
		new_dict['registro'] = self.registro
		return new_dict