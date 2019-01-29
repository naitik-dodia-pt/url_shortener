from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_hashing import Hashing
from flask_caching import Cache
#from redis import Redis
from config import config, Config
from celery import Celery
from datetime import timedelta

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
hashing = Hashing()
cache = Cache(config={'CACHE_TYPE': 'redis'})
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.conf.update(
    CELERYBEAT_SCHEDULE = {
        'hello' : {
            'task' : '__init__.print_hello',
            'schedule' : timedelta(seconds = 5)
        }
    }
)
#redis = Redis()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    hashing.init_app(app)
    cache.init_app(app)

    celery.conf.update(app.config)
    #redis.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    # attach routes and custom error pages here

    return app

@celery.task
def print_hello():
    print("hello")

def hello():
    print_hello.delay()