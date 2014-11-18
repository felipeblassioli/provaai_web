# -*- coding: utf-8 -*-
class Configuration(object):
	"""Default configuration for the application
	"""
	#: Application's root directory.
	DIR_ROOT = '/var/www/provaai'
	#: Uploaded files root directory.
	UPLOADED_DEFAULT_DEST = DIR_ROOT + '/uploads'
	#: Uploaded videos directory.
	UPLOADED_VIDEOS_DEST = UPLOADED_DEFAULT_DEST + '/videos'
	#: Uploaded images directory.
	UPLOADED_IMAGES_DEST = UPLOADED_DEFAULT_DEST + '/images'
	#: Maximum file size that is accepted by the application.
	UPLOADED_MAX_FILE_SIZE = 128 * 1024 * 1024
	#: Database connection settings.
	DATABASE = {
		'name': 'provaai',
		'engine': 'peewee.MySQLDatabase',
		'user': 'root',
		'passwd': '123456'
	}
	#: Log file for the application
	LOG_FILENAME = DIR_ROOT + '/provaai.log'
	#: Prints verbose logging (such as all SQL queries) if set to True.
	DEBUG = True
	SECRET_KEY = 'SOME_MUCH_SECRETE_KEY'
	WTF_CSRF_ENABLED = False