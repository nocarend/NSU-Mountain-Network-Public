import os
from datetime import timedelta

from dotenv import load_dotenv

from app.loader import load_components_requests, load_components_responses

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'TestDB.db')
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	# os.environ.get('DATABASE_URL', '').replace('postgres://',
	# 'postgresql://')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_USE_TLS = 1
	MAIL_MAX_EMAILS = 1000
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = os.environ.get('ADMINS')

	SECRET_KEY = os.environ.get('SECRET_KEY')
	JWT_ACCESS_LIFESPAN = {"hours": 24}
	JWT_REFRESH_LIFESPAN = {"days": 30}
	schemas = load_components_responses()
	schemas.update(load_components_requests())
	SWAGGER = {
		"uiversion":  3,
		"openapi":    "3.0.3",
		"info":       {
			"title":       "My API",
			"description": "Awesome API.",
			"version":     "0.1.0",
			},
		'components': {
			'schemas':         schemas,
			"securitySchemes": {
				"bearerAuth": {
					"type":         "http",
					"scheme":       "bearer",
					"bearerFormat": "JWT",
					'description':  'Put token in given format:eyJhyyy.xxxx'
					}
				}
			}
		}

# LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')  # for heroku
