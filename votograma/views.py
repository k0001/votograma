# coding: utf-8

# Votograma, aplicación web para facilitar la detección de inconsistencias en
# el recuento de votos de las elecciones argentinas del 2011.
# Copyright (C) 2011 Renzo Carbonara <renzo @carbonara punto com punto ar>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
from   operator import itemgetter
from   flask import render_template, jsonify, request
from   votograma import app
from   votograma.models import db, Mesa


@app.route('/')
def index():
    q = Mesa.query.with_entities(Mesa.distrito_tp_id).distinct()
    distritos = [{'distrito_tp_id': x.distrito_tp_id} for x in q.all()]
    return render_template('index.html', distritos=distritos)


@app.route('/distritos.json')
def distritos_json():
    q = Mesa.query
    distrito_tp_id = request.args.get('distrito_tp_id')
    if distrito_tp_id:
        q = q.filter(Mesa.distrito_tp_id==distrito_tp_id)
    q = q.with_entities(Mesa.distrito_tp_id).distinct()
    distritos = [{'distrito_tp_id': x.seccion_tp_id} for x in q.all()]
    return jsonify(distritos=distritos)

@app.route('/secciones.json')
def secciones_json():
    q = Mesa.query
    distrito_tp_id = request.args.get('distrito_tp_id')
    if distrito_tp_id:
        q = q.filter(Mesa.distrito_tp_id==distrito_tp_id)
    seccion_tp_id = request.args.get('seccion_tp_id')
    if seccion_tp_id:
        q = q.filter(Mesa.seccion_tp_id==seccion_tp_id)
    q = q.with_entities(Mesa.seccion_tp_id,
                        Mesa.distrito_tp_id).distinct()
    secciones = [{'seccion_tp_id': x.seccion_tp_id,
                  'distrito_tp_id': x.distrito_tp_id} for x in q.all()]
    return jsonify(secciones=secciones)

@app.route('/circuitos.json')
def circuitos_json():
    q = Mesa.query
    distrito_tp_id = request.args.get('distrito_tp_id')
    if distrito_tp_id:
        q = q.filter(Mesa.distrito_tp_id==distrito_tp_id)
    seccion_tp_id = request.args.get('seccion_tp_id')
    if seccion_tp_id:
        q = q.filter(Mesa.seccion_tp_id==seccion_tp_id)
    circuito_tp_id = request.args.get('circuito_tp_id')
    if circuito_tp_id:
        q = q.filter(Mesa.circuito_tp_id==circuito_tp_id)
    q = q.with_entities(Mesa.circuito_tp_id,
                        Mesa.seccion_tp_id,
                        Mesa.distrito_tp_id).distinct()
    circuitos = [{'circuito_tp_id': x.circuito_tp_id,
                  'seccion_tp_id': x.seccion_tp_id,
                  'distrito_tp_id': x.distrito_tp_id}
                 for x in q.all()]
    return jsonify(circuitos=circuitos)

@app.route('/mesas.json')
def mesas_json():
    q = Mesa.query
    distrito_tp_id = request.args.get('distrito_tp_id')
    if distrito_tp_id:
        q = q.filter(Mesa.distrito_tp_id==distrito_tp_id)
    seccion_tp_id = request.args.get('seccion_tp_id')
    if seccion_tp_id:
        q = q.filter(Mesa.seccion_tp_id==seccion_tp_id)
    circuito_tp_id = request.args.get('circuito_tp_id')
    if circuito_tp_id:
        q = q.filter(Mesa.circuito_tp_id==circuito_tp_id)
    mesa_tp_id = request.args.get('mesa_tp_id')
    if mesa_tp_id:
        q = q.filter(Mesa.mesa_tp_id==mesa_tp_id)
    mesas = [{'id': x.id,
              'mesa_tp_id': x.mesa_tp_id,
              'circuito_tp_id': x.circuito_tp_id,
              'seccion_tp_id': x.seccion_tp_id,
              'distrito_tp_id': x.distrito_tp_id,
              'telegrama_png_url': x.telegrama_png_url,
              'telegrama_pdf_url': x.telegrama_pdf_url}
             for x in q.all()]
    return jsonify(mesas=mesas)

