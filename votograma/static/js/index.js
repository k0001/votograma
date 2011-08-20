(function() {
  /*
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
  */  var app, index_page;
  index_page = {
    empty_secciones: function() {
      return $("#secciones").empty();
    },
    empty_circuitos: function() {
      return $("#circuitos").empty();
    },
    empty_mesas: function() {
      return $("#mesas").empty();
    },
    set_active_distrito: function(opts) {
      var did;
      did = opts.distrito_tp_id;
      $("#distritos .distrito.active").removeClass("active");
      return $("#distritos .distrito[data-distrito_tp_id=" + did + "]").addClass("active");
    },
    set_active_seccion: function(opts) {
      var did, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id], did = _ref[0], sid = _ref[1];
      this.set_active_distrito(opts);
      $("#secciones .seccion.active").removeClass("active");
      return $("#secciones .seccion[data-distrito_tp_id=" + did + "][data-seccion_tp_id=" + sid + "]").addClass("active");
    },
    set_active_circuito: function(opts) {
      var cid, did, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id], did = _ref[0], sid = _ref[1], cid = _ref[2];
      this.set_active_distrito(opts);
      this.set_active_seccion(opts);
      $("#circuitos .circuito.active").removeClass("active");
      return $("#circuitos .circuito[data-distrito_tp_id=" + did + "][data-seccion_tp_id=" + sid + "][data-circuito_tp_id=" + cid + "]").addClass("active");
    },
    set_active_mesa: function(opts) {
      var cid, did, mid, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id, opts.mesa_tp_id], did = _ref[0], sid = _ref[1], cid = _ref[2], mid = _ref[3];
      this.set_active_distrito(opts);
      this.set_active_seccion(opts);
      this.set_active_circuito(opts);
      $("#mesas .mesa.active").removeClass("active");
      return $("#mesas .mesa[data-distrito_tp_id=" + did + "][data-seccion_tp_id=" + sid + "][data-circuito_tp_id=" + cid + "][data-mesa_tp_id=" + mid + "]").addClass("active");
    },
    add_seccion: function(opts) {
      var did, el, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id], did = _ref[0], sid = _ref[1];
      el = $('<a class="seccion"></a>');
      el.text(sid);
      el.attr('href', "#/" + did + "/" + sid);
      el.attr('data-distrito_tp_id', did);
      el.attr('data-seccion_tp_id', sid);
      $("#secciones").append(el);
      return el;
    },
    add_circuito: function(opts) {
      var cid, did, el, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id], did = _ref[0], sid = _ref[1], cid = _ref[2];
      el = $('<a class="circuito"></a>');
      el.text(cid);
      el.attr('href', "#/" + did + "/" + sid + "/" + cid);
      el.attr('data-distrito_tp_id', did);
      el.attr('data-seccion_tp_id', sid);
      el.attr('data-circuito_tp_id', cid);
      $("#circuitos").append(el);
      return el;
    },
    add_mesa: function(opts) {
      var cid, did, el, mid, sid, _ref;
      _ref = [opts.distrito_tp_id, opts.seccion_tp_id, opts.circuito_tp_id, opts.mesa_tp_id], did = _ref[0], sid = _ref[1], cid = _ref[2], mid = _ref[3];
      el = $('<div class="mesa"></div>');
      el.text(mid);
      el.attr('href', "#/" + did + "/" + sid + "/" + cid + "/" + mid);
      el.attr('data-distrito_tp_id', did);
      el.attr('data-seccion_tp_id', sid);
      el.attr('data-circuito_tp_id', cid);
      el.attr('data-mesa_tp_id', mid);
      $("#mesas").append(el);
      return el;
    },
    populate_secciones: function(opts) {
      if (index_page.current_distrito_tp_id !== opts.distrito_tp_id) {
        return $.getJSON("/secciones.json", {
          distrito_tp_id: opts.distrito_tp_id
        }, function(data) {
          var seccion, _fn, _i, _len, _ref;
          index_page.empty_secciones();
          index_page.set_active_distrito(opts);
          _ref = data.secciones;
          _fn = function() {
            return index_page.add_seccion(seccion);
          };
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            seccion = _ref[_i];
            _fn();
          }
          return index_page.current_distrito_tp_id = opts.distrito_tp_id;
        });
      }
    },
    populate_circuitos: function(opts) {
      if (index_page.current_distrito_tp_id !== opts.distrito_tp_id || index_page.current_seccion_tp_id !== opts.seccion_tp_id) {
        return $.getJSON("/circuitos.json", {
          distrito_tp_id: opts.distrito_tp_id,
          seccion_tp_id: opts.seccion_tp_id
        }, function(data) {
          var circuito, _fn, _i, _len, _ref;
          index_page.empty_circuitos();
          index_page.set_active_seccion(opts);
          _ref = data.circuitos;
          _fn = function() {
            return index_page.add_circuito(circuito);
          };
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            circuito = _ref[_i];
            _fn();
          }
          index_page.current_distrito_tp_id = opts.distrito_tp_id;
          return index_page.current_seccion_tp_id = opts.seccion_tp_id;
        });
      }
    },
    populate_mesas: function(opts) {
      if (index_page.current_distrito_tp_id !== opts.distrito_tp_id || index_page.current_seccion_tp_id !== opts.seccion_tp_id || index_page.current_circuito_tp_id !== opts.circuito_tp_id) {
        return $.getJSON("/mesas.json", {
          distrito_tp_id: opts.distrito_tp_id,
          seccion_tp_id: opts.seccion_tp_id,
          circuito_tp_id: opts.circuito_tp_id
        }, function(data) {
          var mesa, _fn, _i, _len, _ref;
          index_page.empty_mesas();
          index_page.set_active_circuito(opts);
          _ref = data.mesas;
          _fn = function() {
            return index_page.add_mesa(mesa);
          };
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            mesa = _ref[_i];
            _fn();
          }
          index_page.current_distrito_tp_id = opts.distrito_tp_id;
          index_page.current_seccion_tp_id = opts.seccion_tp_id;
          return index_page.current_circuito_tp_id = opts.circuito_tp_id;
        });
      }
    }
  };
  app = Sammy("#main", function() {
    this.get("#/", function(context) {
      index_page.empty_mesas();
      index_page.empty_circuitos();
      return index_page.empty_secciones();
    });
    this.get("#/:distrito_tp_id", function(context) {
      var opts;
      opts = {
        distrito_tp_id: this.params['distrito_tp_id']
      };
      index_page.populate_secciones(opts);
      index_page.empty_circuitos();
      return index_page.empty_mesas();
    });
    this.get("#/:distrito_tp_id/:seccion_tp_id", function(context) {
      var opts;
      opts = {
        distrito_tp_id: this.params['distrito_tp_id'],
        seccion_tp_id: this.params['seccion_tp_id']
      };
      index_page.populate_secciones(opts);
      index_page.populate_circuitos(opts);
      return index_page.empty_mesas();
    });
    return this.get("#/:distrito_tp_id/:seccion_tp_id/:circuito_tp_id", function(context) {
      var opts;
      opts = {
        distrito_tp_id: this.params['distrito_tp_id'],
        seccion_tp_id: this.params['seccion_tp_id'],
        circuito_tp_id: this.params['circuito_tp_id']
      };
      index_page.populate_secciones(opts);
      index_page.populate_circuitos(opts);
      return index_page.populate_mesas(opts);
    });
  });
  jQuery(function() {
    return app.run("#/");
  });
}).call(this);
