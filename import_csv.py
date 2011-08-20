#!/usr/bin/env python
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


import logging
import csv
import sys
from   votograma.models import db, Mesa


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def import_csv(f):
    cr = csv.DictReader(f)
    try:
        for row in cr:
            m = Mesa()
            m.distrito_tp_id = row['distrito_id']
            m.seccion_tp_id = row['seccion_id']
            m.circuito_tp_id = row['circuito_id']
            m.mesa_tp_id = row['mesa_id']
            log.info(u"Created Mesa {}".format(m))
            db.session.add(m)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
      import_csv(f)
