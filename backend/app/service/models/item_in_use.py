from app import db
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError,\
	MoneyError, StockError
from app.models.item_in_use import ItemInUse


def item_in_use_prolong_s(use_ids, user):
	if use_ids is None:
		raise JSONNotEnoughError()
	for i in use_ids:
		item = ItemInUse.search_by_use_id(i['use_id'])
		days = i['days']
		if days is None:
			days = 30
		if item is None:
			raise ElementNotFoundError()
		if user.user_money < 0:
			raise MoneyError()
		if (
				'admin' not in user.rolenames and 'warehouseman' not in
				user.rolenames and item.user_id != user.user_id) or\
				days < 0:
			raise StockError()
		item.prolong(days)
	db.session.commit()


def item_in_use_get_s(user, user_id_req, type):
	user_id = user.user_id
	if user_id_req is not None and (
			'warehouseman' in user.rolenames or 'admin' in
			user.rolenames):
		user_id = user_id_req
	match type:
		case 'all':
			type = 3
		case 'taken':
			type = 2
		case 'booked':
			type = 1
		case 'requested':
			type = 0
		case 'rejected':
			type = 4
		case 'returned':
			type = 5
	items = ItemInUse.search_by_user(user_id, type)
	return items
