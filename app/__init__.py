import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from config import Config

app = Flask(__name__)  # pylint: disable=invalid-name
app.config.from_object(Config)
login = LoginManager(app)  # pylint: disable=invalid-name
login.login_view = 'login'
db = SQLAlchemy(app)  # pylint: disable=invalid-name
migrate = Migrate(app, db)  # pylint: disable=invalid-name


def debug_part():
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None  # pylint: disable=invalid-name
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None  # pylint: disable=invalid-name
            if app.config['MAIL_USE_TLS']:
                secure = ()  # pylint: disable=invalid-name
            mail_handler = SMTPHandler(  # pylint: disable=invalid-name
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Microblog Failure',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            # log file
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
                ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Microblog startup')


debug_part()
from app import routes, models, errors
