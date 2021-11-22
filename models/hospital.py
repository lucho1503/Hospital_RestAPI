#!/usr/bin/python3
"""
clase hospital hereda de BaseModel
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

"tabla para relacion many to many con servicios"
servicios_hospital = Table('servicios_hospital', Base.metadata,
						Column('hospital_id', String(60),
							ForeignKey('hospitales.id', onupdate='CASCADE',
										ondelete='CASCADE'),
							primary_key=True),
						Column('servicio_id', String(60),
								ForeignKey('servicios.servicio', onupdate='CASCADE',
											ondelete='CASCADE'),
								primary_key=True))

class Hospital(BaseModel, Base):
	""" 
	atributos y metodos de la clase hospital
	"""
	__tablename__ = 'hospitales'
	medico = relationship("Medico", backref="hospital_med")
	medico_observaciones = relationship("Observacion", backref="hospital_ob")
	pacientes = relationship("Paciente", backref="hospital_paci")
	servicios = relationship("Servicio", secondary="servicios_hospital",
								backref="hospital", viewonly=False)


	def registro(self):
		"""
		busca un registro apartir del objeto
		"""
		registros = models.storage.query_registros()
		registros_propios = []
		for registro in registros:
			if registro.hospital_id == self.id:
				registros_propios.append(registro.to_dict())
		return registros_propios