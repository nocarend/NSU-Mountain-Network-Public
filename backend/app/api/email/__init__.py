from flask import Blueprint

bp = Blueprint('email', __name__)

from . import routes
