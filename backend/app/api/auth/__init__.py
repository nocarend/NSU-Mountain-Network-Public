from flask import Blueprint

from .my_profile import bp as my_profile_bp

bp = Blueprint('auth', __name__)
bp.register_blueprint(my_profile_bp, url_prefix='/my_profile')

from . import routes, admins
