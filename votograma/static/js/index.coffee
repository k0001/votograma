###
Votograma, aplicación web para facilitar la detección de inconsistencias en
el recuento de votos de las elecciones argentinas del 2011.
Copyright (C) 2011 Renzo Carbonara <renzo @carbonara punto com punto ar>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###


index_page =
  empty_secciones: -> $("#secciones").empty()
  empty_circuitos: -> $("#circuitos").empty()
  empty_mesas: -> $("#mesas").empty()

  set_active_distrito: (opts) ->
    did = opts.distrito_tp_id
    $("#distritos .distrito.active").removeClass("active")
    $("#distritos .distrito[data-distrito_tp_id=#{did}]").addClass("active")

  set_active_seccion: (opts) ->
    [did, sid] = [opts.distrito_tp_id, opts.seccion_tp_id]
    this.set_active_distrito(opts)
    $("#secciones .seccion.active").removeClass("active")
    $("#secciones .seccion[data-distrito_tp_id=#{did}][data-seccion_tp_id=#{sid}]").addClass("active")

  set_active_circuito: (opts) ->
    [did, sid, cid] = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id]
    this.set_active_distrito(opts)
    this.set_active_seccion(opts)
    $("#circuitos .circuito.active").removeClass("active")
    $("#circuitos .circuito[data-distrito_tp_id=#{did}][data-seccion_tp_id=#{sid}][data-circuito_tp_id=#{cid}]").addClass("active")

  set_active_mesa: (opts) ->
    [did, sid, cid, mid] = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id, opts.mesa_tp_id]
    this.set_active_distrito(opts)
    this.set_active_seccion(opts)
    this.set_active_circuito(opts)
    $("#mesas .mesa.active").removeClass("active")
    $("#mesas .mesa[data-distrito_tp_id=#{did}][data-seccion_tp_id=#{sid}][data-circuito_tp_id=#{cid}][data-mesa_tp_id=#{mid}]").addClass("active")

  add_seccion: (opts) ->
    [did, sid] = [opts.distrito_tp_id, opts.seccion_tp_id]
    el = $('<a class="seccion"></a>')
    el.text(sid)
    el.attr('href', "#/#{did}/#{sid}")
    el.attr('data-distrito_tp_id', did)
    el.attr('data-seccion_tp_id', sid)
    $("#secciones").append(el)
    el

  add_circuito: (opts) ->
    [did, sid, cid] = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id]
    el = $('<a class="circuito"></a>')
    el.text(cid)
    el.attr('href', "#/#{did}/#{sid}/#{cid}")
    el.attr('data-distrito_tp_id', did)
    el.attr('data-seccion_tp_id', sid)
    el.attr('data-circuito_tp_id', cid)
    $("#circuitos").append(el)
    el

  add_mesa: (opts) ->
    [did, sid, cid, mid] = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id, opts.mesa_tp_id]
    el = $('<div class="mesa"></div>')
    el.text(mid)
    el.attr('href', "#/#{did}/#{sid}/#{cid}/#{mid}")
    el.attr('data-distrito_tp_id', did)
    el.attr('data-seccion_tp_id', sid)
    el.attr('data-circuito_tp_id', cid)
    el.attr('data-mesa_tp_id', mid)
    $("#mesas").append(el)
    el

  populate_secciones: (opts) ->
    if index_page.current_distrito_tp_id != opts.distrito_tp_id
      $.getJSON "/secciones.json", {
          distrito_tp_id: opts.distrito_tp_id
      }, (data) ->
        index_page.empty_secciones()
        index_page.set_active_distrito(opts)
        for seccion in data.secciones
          do ->
            index_page.add_seccion(seccion)
        index_page.current_distrito_tp_id = opts.distrito_tp_id

  populate_circuitos: (opts) ->
    if index_page.current_distrito_tp_id != opts.distrito_tp_id \
        or index_page.current_seccion_tp_id != opts.seccion_tp_id
      $.getJSON "/circuitos.json", {
          distrito_tp_id: opts.distrito_tp_id
          seccion_tp_id: opts.seccion_tp_id
      }, (data) ->
        index_page.empty_circuitos()
        index_page.set_active_seccion(opts)
        for circuito in data.circuitos
          do ->
            index_page.add_circuito(circuito)
        index_page.current_distrito_tp_id = opts.distrito_tp_id
        index_page.current_seccion_tp_id = opts.seccion_tp_id

  populate_mesas: (opts) ->
    if index_page.current_distrito_tp_id != opts.distrito_tp_id \
        or index_page.current_seccion_tp_id != opts.seccion_tp_id \
        or index_page.current_circuito_tp_id != opts.circuito_tp_id
      $.getJSON "/mesas.json", {
          distrito_tp_id: opts.distrito_tp_id
          seccion_tp_id: opts.seccion_tp_id
          circuito_tp_id: opts.circuito_tp_id
      }, (data) ->
        index_page.empty_mesas()
        index_page.set_active_circuito(opts)
        for mesa in data.mesas
          do ->
            index_page.add_mesa(mesa)
        index_page.current_distrito_tp_id = opts.distrito_tp_id
        index_page.current_seccion_tp_id = opts.seccion_tp_id
        index_page.current_circuito_tp_id = opts.circuito_tp_id


app = Sammy "#main", ->

  this.get "#/", (context) ->
    index_page.empty_mesas()
    index_page.empty_circuitos()
    index_page.empty_secciones()

  # Populate secciones
  this.get "#/:distrito_tp_id", (context) ->
    opts =
      distrito_tp_id: this.params['distrito_tp_id']
    index_page.populate_secciones(opts)
    index_page.empty_circuitos()
    index_page.empty_mesas()

  # Populate circuitos & related mesas
  this.get "#/:distrito_tp_id/:seccion_tp_id", (context) ->
    opts =
      distrito_tp_id: this.params['distrito_tp_id']
      seccion_tp_id: this.params['seccion_tp_id']
    index_page.populate_secciones(opts)
    index_page.populate_circuitos(opts)
    index_page.empty_mesas()

  # Populate mesas
  this.get "#/:distrito_tp_id/:seccion_tp_id/:circuito_tp_id", (context) ->
    opts =
      distrito_tp_id: this.params['distrito_tp_id']
      seccion_tp_id: this.params['seccion_tp_id']
      circuito_tp_id: this.params['circuito_tp_id']
    index_page.populate_secciones(opts)
    index_page.populate_circuitos(opts)
    index_page.populate_mesas(opts)

jQuery ->
  app.run("#/")
