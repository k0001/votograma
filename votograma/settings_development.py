import os
here_path = os.path.abspath(os.path.dirname(__file__))

from votograma.settings_base import *

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db_dev.sqlite'.format(here_path)
SQLALCHEMY_ECHO = True

del here_path
