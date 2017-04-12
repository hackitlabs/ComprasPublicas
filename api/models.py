#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Numeric, \
  Unicode, UnicodeText, CHAR, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

Entity = declarative_base()


class buyer(Entity):
  __tablename__ = 'buyer'

  id = Column(Integer, primary_key=True)
  ruc_entidad = Column(UnicodeText, nullable=False)
  nombre = Column(UnicodeText, nullable=False)
  tipo_entidad = Column(UnicodeText, nullable=False)
  nivel_gobierno = Column(UnicodeText, nullable=False)
  dependencia = Column(UnicodeText, nullable=True)
  contrato = relationship("_contrato")
  #hash = Column(UnicodeText, nullable=False)


class _representante(Entity):
  __tablename__ = 'representante'

  id = Column(Integer, primary_key=True)
  dni = Column(CHAR(20), nullable=False)
  nombre = Column(UnicodeText, nullable=False)


class _empresa(Entity):
  __tablename__ = 'empresa'

  id = Column(Integer, primary_key=True)
  ruc = Column(Unicode(255), nullable=False)
  razon_social = Column(UnicodeText, nullable=False)
  consorcio = Column(Integer, default=0)
  nombre_comercial = Column(UnicodeText, nullable=True)
  inicio_actividades = Column(DateTime(timezone=True))
  actividades_com_ext = Column(UnicodeText)
  telefono = Column(UnicodeText)
  fax = Column(UnicodeText)
  estado = Column(UnicodeText)
  condicion = Column(UnicodeText)
  direccion = Column(UnicodeText)
  total_ganado = Column(Numeric(15, 2), nullable=True, default=0)
  update = Column(Integer, default=0)
  persona = Column(Integer, ForeignKey('representante.id'))


class _miembroConsorcio(Entity):
  __tablename__ = 'miembro_consorcio'

  id = Column(Integer, primary_key=True)
  consorcio_id = Column(Integer, ForeignKey('empresa.id'), nullable=True)
  miembro_id = Column(Integer, ForeignKey('empresa.id'), nullable=True)
  contrato_id = Column(Integer, ForeignKey('contrato.id'), nullable=True)


class _loadEmpresa(Entity):
  __tablename__ = 'load_empresa'

  id = Column(Integer, primary_key=True)
  empresa_id = Column(Integer)
  fecha_carga = Column(DateTime(timezone=True), default=datetime.now)
  fecha_actualizacion = Column(DateTime(timezone=True), default=datetime.now)


class _sucursal(Entity):
  __tablename__ = 'sucursal'

  id = Column(Integer, primary_key=True)
  empresa_id = Column(Integer, ForeignKey('empresa.id'))
  tipo = Column(UnicodeText, nullable=False)
  direccion = Column(UnicodeText, nullable=False)


class _contrato(Entity):
  __tablename__ = 'contrato'

  id = Column(Integer, primary_key=True)
  codigo = Column(UnicodeText, nullable=True)
  nro_contrato = Column(UnicodeText, nullable=True)
  descripcion = Column(UnicodeText, nullable=True)
  fecha_publicacion = Column(DateTime(timezone=True))
  fecha_contrato = Column(DateTime(timezone=True))
  fecha_registro_contrato = Column(DateTime(timezone=True))
  fecha_inicio = Column(DateTime(timezone=True))
  fecha_fin = Column(DateTime(timezone=True))
  proceso = Column(UnicodeText, nullable=True)
  modalidad = Column(UnicodeText, nullable=True) 
  tipo_proceso = Column(UnicodeText, nullable=True)
  nro_convocatoria = Column(UnicodeText, nullable=True)
  objeto = Column(UnicodeText, nullable=True)
  objeto_descripcion = Column(UnicodeText, nullable=True)
  valor_referencial = Column(Numeric(15, 2), nullable=True, default=0)
  monto = Column(Numeric(15, 2), nullable=True, default=0)
  tipo_moneda = Column(VARCHAR, default='S/.')
  modalidad_sel = Column(UnicodeText, nullable=True)
  link_contrato = Column(VARCHAR, nullable=True)
  link_seace = Column(VARCHAR, nullable=True, default='ninguna')
  version_seace = Column(VARCHAR, nullable=True, default='seace 2')
  year = Column(VARCHAR, nullable=True, default='seace 2')
  empresa_id = Column(Integer, ForeignKey('empresa.id'))
  destino_pago_id = Column(Integer, ForeignKey('empresa.id'))
  miembro_id = Column(Integer, ForeignKey('empresa.id'))
  entidad_id = Column(Integer, ForeignKey('buyer.id'))

class _itemContrato(Entity):
  __tablename__ = 'item_contrato'

  id = Column(Integer, primary_key=True)
  nro_item = Column(UnicodeText, nullable=True)
  descripcion_item = Column(UnicodeText, nullable=True)
  vref_item = Column(Numeric(15, 2), nullable=True, default=0)
  monto_item = Column(Numeric(15, 2), nullable=True, default=0)
  contrato_id = Column(Integer, ForeignKey('contrato.id'))


if __name__ == '__main__':

  from sqlalchemy import create_engine

  import settings

  db_engine = create_engine(
      settings.DATABASE_DSN,
      echo=settings.DEBUG
  )
  Entity.metadata.create_all(db_engine)
  
  db = sessionmaker(bind=db_engine)()

  _buyer = buyer()
  _buyer.ruc_entidad = '20131372931'
  _buyer.nombre = 'Ministerio de Agricultura'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20504774288'
  _buyer.nombre = 'Ministerio de Comercio Exterior'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20537630222'
  _buyer.nombre = 'Ministerio de Cultura'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131367938'
  _buyer.nombre = 'Ministerio de Defensa'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20545565359'
  _buyer.nombre = 'Ministerio de Desarrollo e Inclusión Social'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131370645'
  _buyer.nombre = 'Ministerio de Economía y Finanzas'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131370998'
  _buyer.nombre = 'Ministerio de Educación'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131368829'
  _buyer.nombre = 'Ministerio de Energía y Minas'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)
  
  _buyer = buyer()
  _buyer.ruc_entidad = '20131371617'
  _buyer.nombre = 'Ministerio de Justicia'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20492966658'
  _buyer.nombre = 'Ministerio del Ambiente'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20336951527'
  _buyer.nombre = 'Ministerio de la Mujer y Poblaciones Vulnerables'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20504794637'
  _buyer.nombre = 'Ministerio de la Producción'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131366966'
  _buyer.nombre = 'Ministerio del Interior'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131380101'
  _buyer.nombre = 'Ministerio de Relaciones Exteriores'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131373237'
  _buyer.nombre = 'Ministerio de Salud'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131023414'
  _buyer.nombre = 'Ministerio de Trabajo y Promoción del Empleo'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20131379944'
  _buyer.nombre = 'Ministerio de Transportes y Comunicaciones'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20504743307'
  _buyer.nombre = 'Ministerio de Vivienda, Construcción y Saneamiento'
  _buyer.tipo_entidad = 'ministerio'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  _buyer = buyer()
  _buyer.ruc_entidad = '20168999926'
  _buyer.nombre = 'Presidencia del Consejo de Ministros'
  _buyer.tipo_entidad = 'oficina_gobierno'
  _buyer.nivel_gobierno = 'poder_ejecutivo'
  db.add(_buyer)

  db.commit()
