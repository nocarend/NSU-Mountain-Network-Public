from flask import Blueprint

from .settings import bp as settings_bp

bp = Blueprint('my_profile', __name__)
bp.register_blueprint(settings_bp, url_prefix='/settings')

from . import routes
