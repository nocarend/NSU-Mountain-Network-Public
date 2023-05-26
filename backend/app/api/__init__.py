from flask import Blueprint

from .auth import bp as auth_bp
from .models import bp as models_bp

bp = Blueprint('api', __name__)
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(models_bp, url_prefix='/models')

