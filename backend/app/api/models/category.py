from flasgger import swag_from
from flask import jsonify, request, Response
from flask_praetorian import auth_required, roles_accepted

from app.api.models import bp
from app.helpers.functions import get_category_data
from app.models.category import Category
from app.service.models.category import category_get_s, category_id_delete_s,\
	category_id_get_s, category_id_patch_s, category_post_s


@bp.route('/categories', methods=['GET'])
@auth_required
@swag_from('yaml/category/category_get.yaml')
def category_get():
	return jsonify(categories=category_get_s())


@bp.route('/categories', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/category/category_post.yaml')
def category_post():
	req = request.get_json(force=True)
	name, weight = get_category_data(req)
	category_post_s(name, weight)
	return Response(status=200)


@bp.route('/categories/<id>', methods=['DELETE'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/category/category_id_delete.yaml')
def category_id_delete(id):
	# наверное, нужно запрещать удаление катоегории когда в ней ещё есть
	# предметы
	category = Category.search_by_id(id)
	category_id_delete_s(category)
	return Response(status=200)

@bp.route('/categories/<id>', methods=['PATCH'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/category/category_id_patch.yaml')
def category_id_patch(id):
	req = request.get_json(force=True)
	name, weight = get_category_data(req)
	category_id_patch_s(id, name, weight)
	return Response(status=200)


@bp.route('/categories/<id>', methods=['GET'])
@auth_required
@swag_from('yaml/category/category_id_get.yaml')
def category_id_get(id):
	return category_id_get_s(id)
