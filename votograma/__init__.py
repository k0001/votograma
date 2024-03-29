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


from flask import Flask

app = Flask(__name__)
app.config.from_envvar('VOTOGRAMA_SETTINGS')

import votograma.views

