# -*- coding: utf-8 -*-
"""
    provaai
    ~~~~~~~

    :author: Felipe Blassioli <felipeblassioli@gmail.com>
"""
from flask import Flask
from flask_peewee.db import Database
from flask.ext.uploads import UploadSet, configure_uploads, patch_request_class, IMAGES
from flask.ext.login import LoginManager

import logging

def setup_logging():
	if app.debug:
		peewee_logger = logging.getLogger('peewee')
		peewee_logger.setLevel(logging.DEBUG)
		peewee_logger.addHandler(logging.StreamHandler())

	# from logging import Formatter
	# from logging.handlers import TimedRotatingFileHandler
	# file_handler = TimedRotatingFileHandler(app.config['LOG_FILENAME'], when='D', interval=1, utc=True)
	# file_handler.setLevel(logging.DEBUG)
	# file_handler.setFormatter(Formatter(
	# 	'%(asctime)s %(levelname)s: %(message)s '
	# 	'[in %(pathname)s:%(lineno)d]'
	# ))
	# app.logger.addHandler(file_handler)

	# if app.debug:
	# 	peewee_logger = logging.getLogger('peewee')
	# 	peewee_logger.setLevel(logging.DEBUG)
	# 	peewee_logger.addHandler(logging.StreamHandler())
	# 	peewee_logger.addHandler(file_handler)

__version__ = '2.0'

app = Flask(__name__, static_url_path='')
app.config.from_object('provaai.config.Configuration')
app.config.from_envvar('PROVAAI_SETTINGS', silent=True)
db = Database(app)

setup_logging()

# Extension setup
videos_manager = UploadSet('videos', ('mp4',))
images_manager = UploadSet('images', IMAGES)
configure_uploads(app, (videos_manager,images_manager))
patch_request_class(app, app.config['UPLOADED_MAX_FILE_SIZE'])

from flask.ext import admin
admin = admin.Admin(app, name='Prova Ai')

login_manager = LoginManager()
login_manager.init_app(app)
import api


