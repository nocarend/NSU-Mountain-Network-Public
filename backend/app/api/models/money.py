from flasgger import swag_from
from flask import jsonify
from flask_praetorian import roles_accepted

from app.api.models import bp
from app.models.money_history import MoneyHistory


@roles_accepted('admin', 'treasureman', 'warehouseman')
@bp.route('/money', methods=['GET'])
@swag_from('yaml/money/money_get.yaml')
def money_get():
	return jsonify(history=MoneyHistory.getAll())
