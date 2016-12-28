#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
import datetime
import settings, models
import csv
import os, glob

db_engine = create_engine(
  settings.DATABASE_DSN,
  echo=settings.DEBUG
)
  
db = sessionmaker(bind=db_engine)()

main_path = 'ministerio_agricultura'
dependency_id = '20131372931'

class importData():

  def _init(self, row):
    _c = self._validateContrato(row[26])

    if(_c):
      if(row[21] == 'S'):
        self._insertMiembro(row[24], row[25], _c.empresa_id, _c.id)
      
      _i = self._validateItem(row[13], _c.id)
      if(_i is False):
        self._insertItem(row, _c.id)
      return _c.id
    return self._insertContrato(row)

  def _validateContrato(self, codigo):
    _c = db.query(
      models._contrato
    ).filter(
      models._contrato.codigo == codigo
    )
    return _c.first() if _c.count() > 0 else False

  def _validateItem(self, nro_item, contrato):
    _i = db.query(
      models._itemContrato
    ).filter(
      and_(models._itemContrato.nro_item == nro_item,
        models._itemContrato.contrato_id == contrato
      )
    )
    return _i.first() if _i.count() > 0 else False

  def _insertContrato(self, row):

    _c = models._contrato()
    _c.codigo = row[26]
    _c.nro_contrato = row[27]
    _c.descripcion = row[10]
    _c.fecha_publicacion = datetime.datetime.strptime(row[8],'%d/%m/%y').isoformat()
    _c.fecha_contrato = datetime.datetime.strptime(row[17],'%d/%m/%y').isoformat()
    _c.fecha_registro_contrato = datetime.datetime.strptime(row[18],'%d/%m/%y').isoformat()
    if row[28]:
      _c.fecha_inicio = datetime.datetime.strptime(row[28],'%d/%m/%y').isoformat()

    if row[29]:
      _c.fecha_fin = datetime.datetime.strptime(row[29],'%d/%m/%y').isoformat()
    
    _c.proceso = row[6]
    _c.modalidad = row[4]
    _c.tipo_proceso = row[5]
    _c.nro_convocatoria = row[7]
    _c.objeto = row[9]
    _c.objeto_descripcion = row[10]
    _c.valor_referencial = (row[11]).replace(",",".")
    _c.monto = (row[11]).replace(",",".")
    _c.tipo_moneda = row[12]
    _c.modalidad_sel = row[4]
    _c.link_contrato = row[30]
    _c.version_seace = row[0]
    _c.year = row[1]
    _c.empresa_id = self._insertEmpresa(row[19], row[20])
    _c.destino_pago_id = self._insertEmpresa(row[22], row[23])
    _c.entidad_id = self._getEntidad(row)

    if(row[21] == 'S'):
      _c.miembro_id =  _c.empresa_id
    
    self._save(_c)

    if(row[21] == 'S'):
      self._insertMiembro(row[24], row[25], _c.empresa_id, _c.id)
    
    self._insertItem(row, _c.id)

    return _c.id

  def _getEntidad(self, row):
    ruc = row[2]
    _entidad = db.query(
      models._entidadGobierno
    ).filter(
      models._entidadGobierno.ruc_entidad == ruc
    )
    return _entidad.first().id if _entidad.count() > 0 else self._insertEntidad(row)

  def _insertEntidad(self, row):
    _entidad = models._entidadGobierno()
    _entidad.ruc_entidad = row[2]
    _entidad.nombre = row[3]
    _entidad.tipo_entidad = 'unidad_ejecutora'
    _entidad.nivel_gobierno = 'poder_ejecutivo'
    _entidad.dependencia = dependency_id
    self._save(_entidad)
    return _entidad.id

  def _insertItem(self, row, c):
    _i = models._itemContrato()
    _i.nro_item = row[13]
    _i.descripcion_item = row[14]
    _i.vref_item = (row[15]).replace(",",".")
    _i.monto_item = (row[16]).replace(",",".")
    _i.contrato_id = c
    self._save(_i)
    return _i.id

  def _insertMiembro(self, ruc, razon_social, consorcio, contrato):
    _m = models._miembroConsorcio()
    _m.consorcio_id = consorcio
    _m.miembro_id = self._insertEmpresa(ruc, razon_social)
    _m.contrato_id = contrato
    self._save(_m)
    return _m.id

  def _insertEmpresa(self, ruc, razon_social):
    _id = self._validateEmpresa(ruc)
    if(_id is False):
      _e = models._empresa()
      _e.ruc = ruc
      _e.razon_social = razon_social
      self._save(_e)
      return _e.id
    return _id

  def _validateEmpresa(self, ruc):
    _empresa = db.query(
      models._empresa
    ).filter(
      models._empresa.ruc == ruc
    )
    return _empresa.first().id if _empresa.count() > 0 else False

  def _save(self, rdata):
    db.add(rdata)
    record = db.commit()
    return record

if __name__ == '__main__':

  files = [f for f in glob.glob("_data/*.csv") if os.path.isfile(f)]
  for f in files:
    with open(f, 'rb') as _datafile:
      _data = csv.reader(_datafile)
      for row in _data:
        importData()._init(row)