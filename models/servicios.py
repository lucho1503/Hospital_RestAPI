#!/usr/bin/python3

"""
clase servicios que hereda de BaseModel
"""

import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship
import sqlalchemy as db


class Servicio(Base):
	__tablename__ = 'servicios'
	servicio = Column(String(60), primary_key=True, nullable=False)