from app import db
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError,\
	StockError, ValidationError
from app.models.category import Category


def category_get_s():
	return Category.getAll()


def category_post_s(name, weight):
	if None in [name, weight]:
		raise JSONNotEnoughError()
	if Category.search_by_name(name) is not None:
		raise ValidationError()
	category = Category(category_name=name, category_weight=weight)
	category.add()
	db.session.commit()


def category_id_delete_s(category):
	if category is None:
		raise ElementNotFoundError()
	if category.items():
		raise StockError("First you should delete all items of this "
		                 "category.")
	category.delete()
	db.session.commit()


def category_id_patch_s(id, name=None, weight=None):
	category = Category.search_by_id(id)
	if category is None:
		raise ElementNotFoundError()
	if name is None:
		name = category.category_name
	if weight is None:
		weight = category.category_weight
	if Category.search_by_name(name) is not None:
		raise ValidationError()
	category.category_weight = weight
	category.category_name = name
	db.session.commit()

def category_id_get_s(id):
	category = Category.search_by_id(id)
	if category is None:
		raise ElementNotFoundError()
	response = dict()
	response['category_id'] = category.category_id
	response['category_weight'] = category.category_weight
	response['category_name'] = category.category_name
	response['items'] = category.items()
	return response
