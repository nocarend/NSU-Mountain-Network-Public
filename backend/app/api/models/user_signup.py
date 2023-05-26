from flasgger import swag_from
from flask import Response
from flask_praetorian import roles_accepted

from app.api.models import bp
from app.service.models.user_signup import approve_user_s,\
	reject_user_s, signup_requests_get_s


@bp.route('/signup_requests', methods=['GET'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/user_signup/signup_requests_get.yaml')
def signup_requests_get():
	return signup_requests_get_s()


@bp.route('/signup_requests/approve_user/<signup_id>', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/user_signup/approve_user.yaml')
def approve_user(signup_id):
	user = approve_user_s(signup_id)
	return Response(status=200 if user else 404)


@bp.route('/signup_requests/reject_user/<username>', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/user_signup/reject_user.yaml')
def reject_user(signup_id):
	user = reject_user_s(signup_id)
	return Response(status=200 if user else 404)
