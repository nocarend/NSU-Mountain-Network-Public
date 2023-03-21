from flask import Blueprint


bp = Blueprint('schedules', __name__)

from . import once_a_day
