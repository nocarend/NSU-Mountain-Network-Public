from datetime import datetime

from flasgger import swag_from
from flask import jsonify, request, Response
from flask_praetorian import auth_required, current_rolenames, current_user,\
	roles_accepted

from app import db
from app.api.models import bp
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError,\
	MoneyError, StockError
from app.helpers.functions import get_item_data
from app.models.category import Category
from app.models.item import Item
from app.models.item_in_use import ItemInUse


@bp.route('/items', methods=['GET'])
@auth_required
@swag_from('yaml/item/items_get.yaml')
def items_get():
	items = Item.query.all()
	return jsonify(items=items), 200


@bp.route('/items', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/items_post.yaml')
def items_post():
	req = request.get_json(force=True)
	name, category_id, weight, quantity, cost, description =\
		get_item_data(
			req)
	if None in [name, category_id]:
		raise JSONNotEnoughError()
	if Category.search_by_id(category_id) is None:
		raise ElementNotFoundError()
	newItem = Item(item_name=name, category_id=category_id)
	if weight:
		newItem.item_weight = weight
	if quantity:
		newItem.item_quantity_max = quantity
	if cost:
		newItem.item_cost = cost
	if description:
		newItem.item_description = description
	newItem.add()
	db.session.commit()
	return Response(status=201)


@bp.route('/items/<item_id>', methods=['GET'])
@auth_required
@swag_from('yaml/item/items_item_id_get.yaml')
def items_item_id_get(item_id):
	item = Item.search_by_id(item_id)
	if item is None:
		raise ElementNotFoundError()
	return (jsonify(
		item=item) if 'warehouseman' not in current_rolenames() and 'admin'
	                  not in\
	                  current_rolenames() else jsonify(item=item,
	                                                   item_data=item.users())), 200


@bp.route('/items/<item_id>', methods=['PATCH'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/items_item_id_patch.yaml')
def items_item_id_patch(item_id):
	item = Item.search_by_id(item_id)
	if item is None:
		raise ElementNotFoundError()
	req = request.get_json(force=True)
	name, category_id, weight, quantity, cost, description =\
		get_item_data(
			req)
	if name and category_id is None:
		category_id = item.category_id
	elif category_id and name is None:
		name = item.item_name
	if name:
		item.item_name = name
	if category_id:
		if Category.search_by_id(category_id) is None:
			raise ElementNotFoundError()
		item.category_id = category_id
	if weight:
		item.item_weight = weight
	if quantity:
		item.item_quantity_max = quantity
		if item.item_quantity_current < 0:
			raise StockError()
	if cost:
		item.item_cost = cost
	if description:
		item.item_description = description
	db.session.commit()
	return Response(status=200)


@bp.route('/items/<item_id>', methods=['DELETE'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/items_item_id_delete.yaml')
def items_item_id_delete(item_id):
	item = Item.search_by_id(item_id)
	if item is None:
		raise ElementNotFoundError()
	if item.users():
		raise StockError()
	item.delete()
	db.session.commit()
	return Response(status=204)


@bp.route('/items/<item_id>/image', methods=['GET'])
@auth_required
@swag_from('yaml/item/items_item_id_get_image.yaml')
def items_item_id_get_image(item_id):
	item = Item.search_by_id(item_id)
	if item is None:
		raise ElementNotFoundError()
	return item.avatar(), 200


@bp.route('/items/book', methods=['POST'])
@auth_required
@swag_from('yaml/item/item_book.yaml')
def item_book():
	req = request.get_json()
	items = req.get('items', None)
	if current_user().user_money < 0:
		raise MoneyError()
	if items is None:
		raise JSONNotEnoughError()
	for i in items:
		item = Item.search_by_id(i['item_id'])
		count = i['quantity']
		datetime_from = datetime.strptime(i['datetime_from'], '%Y-%m-%d')
		datetime_to = datetime.strptime(i['datetime_to'], '%Y-%m-%d')
		if item is None:
			raise ElementNotFoundError()
		if count is None or datetime_from is None or datetime_to is None:
			raise JSONNotEnoughError()
		item.book(count, datetime_from, datetime_to)
	db.session.commit()
	return Response(status=200)


# work
@bp.route('/items/use/unbook', methods=['POST'])
@auth_required
@swag_from('yaml/item/item_unbook.yaml')
def item_unbook():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in useIds:
		itemRecord = ItemInUse.search_by_use_id(i['use_id'])
		count = i['quantity']
		if itemRecord is None:
			raise ElementNotFoundError()
		if count is None:
			raise JSONNotEnoughError()
		itemRecord.unbook(count)
	db.session.commit()
	return Response(status=200)


# work
@bp.route('/items/use/return', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/item_return.yaml')
def item_return():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in useIds:
		itemRecord = ItemInUse.search_by_use_id(i['use_id'])
		count = i['quantity']
		if itemRecord is None:
			raise ElementNotFoundError()
		if count is None:
			raise JSONNotEnoughError()
		itemRecord.return_(count)
	db.session.commit()
	return Response(status=200)


# work
@bp.route('/items/use/approve', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/approve_item.yaml')
def approve_item():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in useIds:
		description = i['description']
		use_id = i['use_id']
		ItemInUse.approve(use_id, description)
	db.session.commit()
	return Response(status=200)


@bp.route('/items/use/reject', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/reject_item.yaml')
def reject_item():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in useIds:
		use_id = i['use_id']
		reason = i['description']
		ItemInUse.reject(use_id, reason)
	db.session.commit()
	return Response(status=200)


@bp.route('/items/use/give', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/give_item.yaml')
def give_item():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in useIds:
		use_id = i['use_id']
		ItemInUse.give(use_id)
	db.session.commit()
	return Response(status=200)


@bp.route('/items/use/book_reject', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/book_reject.yaml')
def book_reject():
	req = request.get_json(force=True)
	useIds = req.get('use_ids', None)
	if useIds is None:
		raise JSONNotEnoughError()
	for i in range(len(useIds)):
		use_id = useIds[i]['use_id']
		reason = useIds[i]['description']
		item = ItemInUse.search_by_use_id(use_id)
		item.unbook(useIds[i]['quantity'], 1, reason)
	db.session.commit()
	return Response(status=200)


@bp.route('/items/use/<id>', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/item/request_description_set.yaml')
def request_description_set(id):
	req = request.get_json(force=True)
	description = req.get('description', None)
	if description is None:
		raise JSONNotEnoughError()
	item = ItemInUse.search_by_use_id(id)
	if item is None:
		raise ElementNotFoundError()
	item.use_description = description
	db.session.commit()
	return Response(status=200)
