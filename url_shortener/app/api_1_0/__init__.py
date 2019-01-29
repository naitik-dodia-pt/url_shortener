from flask import Blueprint

api = Blueprint('api', __name__)

from . import url, freeurl, runningurl, views, algorithms, constants, data, errors