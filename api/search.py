#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, and_, or_, func, extract
from sqlalchemy.orm import sessionmaker
from math import ceil
import settings
import models
import re
import datetime

db_engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG
)

db = sessionmaker(bind=db_engine)()


class Contratos():

  def getContrato(self, id):

    _contracto = db.query(
      models._contrato
    ).filter(
      models._contrato.id == id
    ).first()

    return _contracto

  def getEntidad(self, id):

    _entidad = db.query(
      models._entidadGobierno
    ).filter(
      models._entidadGobierno.id == id
    ).first()

    return _entidad

  def getEmpresa(self, id):

    _empresa = db.query(
      models._empresa
    ).filter(
      models._empresa.id == id
    ).first()

    return _empresa

  def getItems(self, id):

    _items = db.query(
      models._itemContrato
    ).filter(
      models._itemContrato.contrato_id == id
    ).all()

    return _items

class Entidad():

  def getContratos(self, id, limit):

    _contractos = db.query(
      models._contrato
    ).filter(
      models._contrato.entidad_id == id
    ).limit(limit).all()

    return _contractos

  def get_objects_by_year(self, id, year):

    _objects = db.query(
      models._contrato.year,
      models._contrato.objeto,
      func.sum(models._contrato.monto).label("total")
    ).filter(
      and_(models._contrato.entidad_id == id,
      models._contrato.year == year)
    ).group_by(models._contrato.year, models._contrato.objeto).all()

    return _objects

  def get_contracts_year(self, id, year):

    _objects = db.query(
      models._contrato.fecha_publicacion,
      func.count(models._contrato.id).label("value"),
      func.sum(models._contrato.monto).label("monto")
    ).filter(
      and_(
        extract('year', models._contrato.fecha_publicacion) == year
      )
    ).order_by(
      models._contrato.fecha_publicacion.desc()
    ).group_by(
      models._contrato.fecha_publicacion
    ).all()

    return _objects


class Empresa():

  def getContratos(self, id, limit):

    _contractos = db.query(
      models._contrato
    ).filter(
      models._contrato.empresa_id == id
    ).limit(limit).all()

    return _contractos