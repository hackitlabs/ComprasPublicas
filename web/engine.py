#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, and_, or_, func, extract, select, distinct
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
      models.buyer
    ).filter(
      models.buyer.id == id
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

  def getAmountsPerYear(self, id, year):
    _objects = db.query(
      extract('month', models._contrato.fecha_contrato).label("mes"),
      func.sum(models._contrato.monto).label("monto")
    ).filter(
      and_(
        models._contrato.entidad_id == id,
        extract('year', models._contrato.fecha_contrato) == year
      )
    ).order_by(
      extract('month', models._contrato.fecha_contrato)
    ).group_by(
      extract('month', models._contrato.fecha_contrato)
    ).all()
    return _objects

  def getAmountsPerObjectYear(self, field, id, year, filter, currency):
    _objects = db.query(
      extract('month', models._contrato.fecha_contrato).label("mes"),
      func.sum(models._contrato.monto).label("monto")
    ).filter(
      and_(
        models._contrato.entidad_id == id,
        extract('year', models._contrato.fecha_contrato) == year,
        getattr(models._contrato, field) == filter,
        models._contrato.tipo_moneda == currency
      )
    ).order_by(
      extract('month', models._contrato.fecha_contrato)
    ).group_by(
      extract('month', models._contrato.fecha_contrato)
    ).all()
    return _objects

  def getObjectsPerYear(self, field, id, year, currency):
    _objects = db.query(
      getattr(models._contrato, field)
    ).filter(
      and_(
        models._contrato.entidad_id == id,
        extract('year', models._contrato.fecha_contrato) == year,
        models._contrato.tipo_moneda == currency
      )
    ).group_by(getattr(models._contrato, field)).all()

    _list = []
    for _o in _objects:
      _amounts = self.getAmountsPerObjectYear(field, id, year, _o[0], currency)
      _values = [0 for _i in range(0, 12)]
      for _a in _amounts:
        _values[int(_a[0])-1] = float(_a[1])
      _list.append({"objeto": (_o[0]).title(), "data": _values})
    return _list

class Entidad():

  def getEntidades(self):
    _entidades = db.query(
        models.buyer.id,
        models.buyer.nombre,
        func.count(distinct(models._contrato.empresa_id)).label("count")
      ).join(
        models._contrato
      ).group_by(
        models.buyer.id
      ).all()
    return _entidades

  def getContratos(self, id, limit):
    _contractos = db.query(
      models._contrato
    ).filter(
      models._contrato.entidad_id == id
    ).limit(limit).all()
    return _contractos

  def getProcesos(self, id, moneda):
    _contratos = db.query(
      models._contrato.tipo_proceso,
      func.count(models._contrato.id).label("contratos"),
      func.count(distinct(models._contrato.empresa_id)).label("empresas"),
      func.sum(models._contrato.monto).label("total")
    ).filter(
      models._contrato.entidad_id == id,
      models._contrato.tipo_moneda == moneda
    ).group_by(
      models._contrato.tipo_proceso
    ).order_by(
      func.count(models._contrato.id).label("contratos").desc()
    ).all()

    return _contratos

  def getTopContratos(self, id, limit):
    _contractos = db.query(
      models._empresa.razon_social,
      models._contrato.descripcion,
      models._contrato.objeto,
      models._contrato.fecha_inicio,
      models._contrato.fecha_fin,
      func.count(models._contrato.id).label("contratos"),
      func.sum(models._itemContrato.monto_item).label("monto"),
      (models._contrato.fecha_fin - models._contrato.fecha_inicio).label("dias"),
    ).join(
      models._contrato, models._empresa.id==models._contrato.empresa_id
    ).join(
      models._itemContrato, models._itemContrato.contrato_id==models._contrato.id
    ).filter(
      models._contrato.entidad_id == id,
      models._contrato.tipo_moneda == 'Soles'
    ).group_by(
      models._empresa.razon_social,models._contrato.descripcion,
      models._contrato.objeto, models._contrato.fecha_inicio, models._contrato.fecha_fin
    ).order_by(
      func.sum(models._contrato.monto).label("monto").desc(),
      func.count(models._contrato.id).label("contratos").desc()
    ).limit(limit).all()

    return _contractos

  def getTopEmpresas(self, id, limit):
    _contractos = db.query(
      models._empresa.ruc,
      models._empresa.razon_social,
      func.count(models._contrato.id).label("contratos"),
      func.sum(models._itemContrato.monto_item).label("monto"),
    ).join(
      models._contrato, models._empresa.id==models._contrato.empresa_id
    ).join(
      models._itemContrato, models._itemContrato.contrato_id==models._contrato.id
    ).filter(
      models._contrato.entidad_id == id,
      models._contrato.tipo_moneda == 'Soles'
    ).group_by(
      models._empresa.ruc, models._empresa.razon_social
    ).order_by(
      func.count(models._contrato.id).label("contratos").desc(),
      func.sum(models._itemContrato.monto_item).label("monto").desc()
    ).limit(limit).all()

    return _contractos

  def getSumaContratos(self, id):
    _contratos = db.query(
        models._contrato.tipo_moneda,
        func.sum(models._contrato.monto).label("total"),
      ).filter(
        models._contrato.entidad_id == id
      ).group_by(
        models._contrato.tipo_moneda
      ).order_by(
        func.sum(models._contrato.monto).label("total").desc()
      ).all()

    return _contratos

  def getResumen(self, id):
    _contractos = db.query(
      func.count(models._contrato.id).label("contratos"),
      func.count(distinct(models._contrato.empresa_id)).label("empresas"),
      func.count(distinct(models._miembro_consorcio.consorcio_id)).label("consorcios"),
      func.count(distinct(models._miembro_consorcio.miembro_id)).label("miembros"),
      func.count(distinct(models._contrato.destino_pago_id)).label("cobraron"),
      func.avg(func.justify_days(models._contrato.fecha_fin - models._contrato.fecha_inicio)).label("dias"),
      func.min(models._contrato.fecha_publicacion).label("fecha")
    ).outerjoin(
      models._miembro_consorcio, models._miembro_consorcio.id==models._contrato.miembro_id
    ).filter(
      models._contrato.entidad_id == id
    ).first()
    return _contractos

  def getCompanies(self, id):
    _companies = db.query(
      models._empresa.ruc,
      models._empresa.razon_social,
      func.count(models._empresa.id)
    ).outerjoin(
      models._contrato, models._contrato.empresa_id==models._empresa.id
    ).filter(
      models._contrato.entidad_id == id
    ).group_by(
      models._empresa.ruc,
      models._empresa.razon_social,
    ).all()
    return _companies

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
      models._contrato.fecha_contrato,
      func.count(models._contrato.id).label("value"),
      func.sum(models._contrato.monto).label("monto")
    ).filter(
      and_(
        models._contrato.entidad_id == id,
        extract('year', models._contrato.fecha_contrato) == year
      )
    ).order_by(
      models._contrato.fecha_contrato.desc()
    ).group_by(
      models._contrato.fecha_contrato
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

  def getTopProveedores(self, entidad_id, type, year):

    contratos = func.count((models._contrato.empresa_id)).label("contratos")
    sum_monto = func.sum((models._contrato.monto)).label("suma_monto")
    _proveedores = db.query(
      models._contrato.empresa_id,
      models._empresa.ruc,
      models._empresa.razon_social,
      contratos,
      sum_monto
    ).filter(
      models._contrato.entidad_id == entidad_id,
      extract('year', models._contrato.fecha_contrato) == year,
      models._empresa.ruc.like("%s%s" % (type, "%"))
    ).group_by(
      models._contrato.empresa_id,
      models._empresa.ruc,
      models._empresa.razon_social
    ).order_by(
      sum_monto.desc()
    ).order_by(
      contratos.desc()
    ).limit(10).all()
    return _proveedores