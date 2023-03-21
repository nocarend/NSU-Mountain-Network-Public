from flask import Blueprint

bp = Blueprint('protected', __name__)

from . import routes
