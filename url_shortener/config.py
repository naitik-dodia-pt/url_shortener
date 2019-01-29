import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    URLSHORTENER_MAIL_SUBJECT_PREFIX = '[URL_Shortener]'
    URLSHORTENER_MAIL_SENDER = 'URL_Shortener Admin <naitik.dodia@proptiger.com>'
    URLSHORTENER_ADMIN = os.environ.get('URLSHORTENER_ADMIN')
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='db+mysql://root@localhost:3306/shurl'
    


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/shurl'
    CACHE_DEFAULT_TIMEOUT = 100
    # CACHE_KEY_PREFIX = 
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    # CACHE_REDIS_PASSWORD
    CACHE_REDIS_DB = 0
    # CACHE_ARGS
    # CACHE_OPTIONS
    # CACHE_REDIS_URL = 'redis://user@localhost:6379/'
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='db+mysql://root@localhost:3306/shurl'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config =  {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,
    'default': DevelopmentConfig
}