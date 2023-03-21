from flask import Blueprint

from .auth import bp as auth_bp
from .email import bp as email_bp
from .models import bp as models_bp
from .protected import bp as protected_bp

bp = Blueprint('api', __name__)
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(email_bp, url_prefix='/email')
bp.register_blueprint(models_bp, url_prefix='/models')
bp.register_blueprint(protected_bp, url_prefix='/protected')

