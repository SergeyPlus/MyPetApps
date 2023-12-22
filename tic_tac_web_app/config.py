import logging
import os
import sys


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    ...


class ProductionConfig(Config):
    ...


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


class LoggerConfig:

    log_config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s : %(module)s : %(funcName)s : %(levelno)s : %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 10,
                'formatter': 'simple',
                'stream': sys.stdout
            }
        },
        'loggers': {
            'wo_logger': {
                'level': 10,
                'handlers': ['console']
            },
            'view_logger': {
                'level': 10,
                'handlers': ['console']

            },
            'db_logger': {
                'level': 10,
                'handlers': ['console']
            }
        }
    }
