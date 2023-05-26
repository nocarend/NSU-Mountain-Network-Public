from flask import Blueprint

bp = Blueprint('models', __name__)

from . import user, category, item, user_salt, user_signup, item_in_use
