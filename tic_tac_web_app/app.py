from flask import Flask
from flask_moment import Moment
from flask_mail import Mail

import logging

from config import config


moment = Moment()
mail = Mail()

logging.basicConfig(level=10, format='%(module)s : %(asctime)s : %(message)s')
app_logger = logging.getLogger(__name__)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    mail.init_app(app)
    return app


if __name__ == '__main__':
    pass