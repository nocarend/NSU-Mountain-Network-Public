import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from zoneinfo import ZoneInfo

import flask_cors
import flask_praetorian
from flasgger import Swagger
from flask import Flask
from flask_apscheduler import APScheduler
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.tokens import is_user_blacklisted
from config import Config

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cors = flask_cors.CORS()
guard = flask_praetorian.Praetorian()
swagger = Swagger()
scheduler = APScheduler()

timezone = ZoneInfo('Asia/Novosibirsk')


# Конфиг
def create_app(config_class=Config):
	import os
	app = Flask(__name__)
	app.config.from_object(config_class)

	# app.app_context().push()
	db.init_app(app)
	migrate.init_app(app, db)
	mail.init_app(app)
	cors.init_app(app)
	swagger.init_app(app)

	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	from app.models import bp as models_bp
	app.register_blueprint(models_bp)

	from app.helpers import bp as helpers_bp
	app.register_blueprint(helpers_bp)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	# from app.service import bp as service_bp
	# app.register_blueprint(service_bp)

	from app.models.user import User
	guard.init_app(app, User, is_blacklisted=is_user_blacklisted)  #
	# authentication

	from app.schedules import bp as schedules_bp
	app.register_blueprint(schedules_bp)

	if not app.debug and not app.testing:
		scheduler.init_app(app)
		scheduler.start()

		if app.config['MAIL_SERVER']:
			auth = None
			if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
				auth = (
					app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
			secure = None
			if app.config['MAIL_USE_TLS']:
				secure = ()
			mail_handler = SMTPHandler(
				mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
				fromaddr='no-reply@' + app.config['MAIL_SERVER'],
				toaddrs=app.config['ADMINS'], subject='nsu Failure',
				credentials=auth, secure=secure)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)
		# if app.config['LOG_TO_STDOUT']:  # for heroku
		# 	stream_handler = logging.StreamHandler()
		# 	stream_handler.setLevel(logging.INFO)
		# 	app.logger.addHandler(stream_handler)
		# else:
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/nmm.log', maxBytes=10240,
		                                   backupCount=10)
		file_handler.setFormatter(logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('nmm startup')
	return app


from app.models import *
