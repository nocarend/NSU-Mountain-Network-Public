from flasgger import swag_from
from flask import jsonify, request, Response
from flask_praetorian import auth_required, current_user

from . import bp
from ...service.models.item_in_use import item_in_use_get_s,\
	item_in_use_prolong_s


@bp.route('/item_in_use/prolong', methods=['POST'])
@auth_required
@swag_from('yaml/item_in_use/item_in_use_prolong.yaml')
def item_in_use_prolong():
	req = request.get_json()
	use_ids = req.get('use_ids', None)
	item_in_use_prolong_s(use_ids, current_user())
	return Response(status=200)


@bp.route('/item_in_use/<type>', methods=['GET'])
@auth_required
@swag_from('yaml/item_in_use/item_in_use_get.yaml')
def item_in_use_get(type):
	req = request.get_json()
	user_id_req = req.get('user_id', None)
	return jsonify(items=item_in_use_get_s(current_user(), user_id_req, type)), 200
