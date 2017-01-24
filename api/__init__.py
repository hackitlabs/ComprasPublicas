#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, g, render_template, json, request, Response, url_for, redirect
from sqlalchemy import create_engine, or_, and_, func, extract, desc, asc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import models, settings, search
import json


app = Flask(
  __name__,
  static_folder=settings.STATIC_PATH,
  static_url_path=settings.STATIC_URL_PATH
  )

db_engine = create_engine(
  settings.DATABASE_DSN,
  echo=settings.DEBUG
  )

months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
           'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

@app.before_request
def before_request():
  g.db = sessionmaker(
    bind=db_engine
    )()


@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

#Template for contract
def generate_contract(id):
  contrato = search.Contratos().getContrato(id)
  entidad = search.Contratos().getEntidad(contrato.entidad_id)
  empresa = search.Contratos().getEmpresa(contrato.entidad_id)
  _items = search.Contratos().getItems(contrato.id)
  items = (',').join([render_template("item.json", item=_i, contrato=contrato) for _i in _items])
  _contrato = render_template("contrato.json", contrato=contrato, empresa=empresa, entidad=entidad, items=items)
  return _contrato

#Return only one ontract
@app.route('/api/get/contract/<int:id>', methods=['GET'])
def get_contract(id):
  date = datetime.utcnow().isoformat()
  _contrato = generate_contract(id)
  _releases = render_template("releases.json", datecallback=date, contratos=_contrato)
  return Response(_releases, content_type='application/json')

#Return contract by Goverment office
@app.route('/api/get/entidad/<int:id>', methods=['GET'])
def get_entity(id):
  date = datetime.utcnow().isoformat()
  _list_contracts = [_e.id for _e in search.Entidad().getContratos(id, 10)]
  _contratos = (',').join([generate_contract(id) for _i in _list_contracts])
  _releases = render_template("releases.json", datecallback=date, contratos=_contratos)
  return Response(_releases, content_type='application/json')

#Return amounts of contracts by goverment office
@app.route('/api/get/amounts/<int:id>/<string:year>', methods=['GET'])
def get_amount_office(id, year):
  _data = [_e for _e in search.Contratos().getObjectsPerYear(id, year)]
  _amounts = [render_template("amount.json", data=_i) for _i in _data]
  _amounts = "[%s]" % (',').join(_amounts)
  return Response(_amounts, content_type='application/json')

#Return amounts of contracts by goverment office
@app.route('/api/get/amounts/<string:field>/<int:office>/<string:year>/<string:currency>', methods=['GET'])
def get_amount_office_object(field, office, year, currency):
  _data = search.Contratos().getObjectsPerYear(field, office, year, currency)
  _amounts = [render_template("amount_objects.json", data=_i) for _i in _data]
  _amounts = "[%s]" % (',').join(_amounts)
  return Response(_amounts, content_type='application/json')

#Return contracts by Company
@app.route('/api/get/empresa/<int:id>', methods=['GET'])
def get_empresa(id):
  date = datetime.utcnow().isoformat()
  _list_contracts = [_e.id for _e in search.Empresa().getContratos(id, 10)]
  _contratos = (',').join([generate_contract(id) for _i in _list_contracts])
  _releases = render_template("releases.json", datecallback=date, contratos=_contratos)
  return Response(_releases, content_type='application/json')

#Return contracts by Company
@app.route('/api/get/graphs/objects_by_year/<int:id>/<string:year>', methods=['GET'])
def get_objects_by_year(id, year):
  date = datetime.utcnow().isoformat()
  _data = search.Entidad().get_objects_by_year(id, year)
  _graph = "[%s]" % (',').join([render_template("group_objects.json", data=_i) for _i in _data])
  return Response(_graph, content_type='application/json')

#Return contracts by Company
@app.route('/api/get/graphs/contrats_year/<int:id>/<string:year>', methods=['GET'])
def get_contracts_by_year(id, year):
  date = datetime.utcnow().isoformat()
  _data = search.Entidad().get_contracts_year(id, year)
  _graph = "[%s]" % (',').join([render_template("group_calendar.json", data=_i) for _i in _data])
  return Response(_graph, content_type='application/json')

#return contracts by 
@app.route('/api/get/search/<string:type>', methods=['GET'])
def get_search(type):
  termino = request.args.get('term')
  searchObj = search.Search()
  entidades, pagination = searchObj.get_results_contrataciones(termino, 1, 5)

  list = []

  for e in entidades:
    list.append(e.descripcion)

    return json.dumps(list)

if __name__ == '__main__':
  app.run(
    debug=settings.DEBUG,
  )