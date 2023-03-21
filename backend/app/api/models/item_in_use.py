from flask import request, Response
from flask_praetorian import auth_required, current_user

from app.api.models import bp
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError, MoneyError
from app.models.item_in_use import ItemInUse


@bp.route('/items_in_use/prolong', methods=['POST'])
@auth_required
def item_in_use_prolong():
	req = request.get_json()
	items = req.get('items', None)
	if items is None:
		raise JSONNotEnoughError()
	for i in items:
		item = ItemInUse.search_by_use_id(i)
		if item is None:
			raise ElementNotFoundError()
		if current_user().user_money < 0:
			raise MoneyError()
		item.prolong()
	return Response(status=200)
