import os
import urllib3
import logging


logger = logging.getLogger(__name__)


class BaseConfig(object):

    # application
    DEBUG = False
    TESTING = False

    # gunicorn
    workers = 4
    backlog = 4096
    bind = "0.0.0.0:8080"
    debug = False
    loglevel = 'warning'

class DevelopmentConfig(BaseConfig):

    # application
    DEBUG = True
    TESTING = True

    # gunicorn
    debug = True
    loglevel = 'debug'
    reload = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    # gunicorn
    graceful_timeout = 180
    timeout = 180
    loglevel = 'info'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    # gunicorn
    graceful_timeout = 180
    timeout = 180


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(environment: str = None) -> BaseConfig:

    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'default')

    logger.debug(
        f"For environment {environment} loading config {config_map[environment].__name__}")

    return config_map[environment]()
