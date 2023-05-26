def none_check(n: int, array):
	return n * [None] == array


def get_user_data(req):
	user_login = req.get('login', None)
	user_password = req.get('password', None)
	user_name = req.get('name', None)
	user_email = req.get('email', None)
	user_phone = req.get('phone', None)
	return user_login, user_password, user_name, user_email, user_phone


def get_item_data(req):
	item_name = req.get('name', None)
	category_id = req.get('category_id', None)
	item_weight = req.get('weight', None)
	item_quantity_max = req.get('quantity', None)
	item_cost = req.get('cost', None)
	item_description = req.get('description', None)
	return item_name, category_id, item_weight, item_quantity_max,\
		item_cost, item_description


def get_category_data(req):
	name = req.get('category_name', None)
	weight = req.get('category_weight', None)
	return name, weight
