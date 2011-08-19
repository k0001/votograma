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

from   flask import url_for
from   flaskext.sqlalchemy import SQLAlchemy
from   votograma import app

__all__ = 'db', 'Mesa',


db = SQLAlchemy(app)


class _AddReprMixin(object):
    def __repr__(self):
        s = u'<%s.%s %s>' % (self.__class__.__module__,
                             self.__class__.__name__, unicode(self))
        return s.encode('utf-8')


class Mesa(db.Model, _AddReprMixin):
    __tablename__ = 'mesa'
    id = db.Column(db.Integer, primary_key=True)

    # 'tp_id' stands for 'Third Party ID'. Also, denormalization ftw.
    distrito_tp_id = db.Column(db.String(7), nullable=False)
    seccion_tp_id = db.Column(db.String(7), nullable=False)
    circuito_tp_id = db.Column(db.String(7), nullable=False)
    mesa_tp_id = db.Column(db.String(7), nullable=False)


    def __unicode__(self):
        return self.slug

    @property
    def slug(self):
        return u'-'.join([self.distrito_tp_id, self.seccion_tp_id,
                          self.circuito_tp_id, self.mesa_tp_id])

    @property
    def telegrama_png_url(self):
        return url_for('static',
                       filename='/static/telegramas/{}.png'.format(self.slug))

    @property
    def telegrama_pdf_url(self):
        d = { 'd': self.distrito_tp_id, 's': self.seccion_tp_id,
              'c': self.circuito_tp_id, 'm': self.mesa_tp_id }
        sep = '_' if d['c'][-1].isdigit() else d['c'][-1]
        d['pdf_filename'] = '{d}{s}{c}{sep}{m}.pdf'.format(sep=sep, **d)
        return (u'http://www.primarias2011.gob.ar/paginas/paginaspdf'
                u'/{d}/{s}/{c}/{pdf_filename}') % d

