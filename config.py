# http://flask.pocoo.org/docs/config/#development-production

import os


class BaseConfig:
    # Run `python2 -c 'import os; print os.urandom(24)'`
    # to generate a random key
    # http://flask.pocoo.org/docs/0.10/quickstart/#sessions
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BOOTSTRAP_SERVE_LOCAL = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
