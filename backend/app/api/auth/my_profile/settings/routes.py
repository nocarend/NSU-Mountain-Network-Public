from flasgger import swag_from
from flask import request, Response
from flask_praetorian import auth_required, current_user

from . import bp


@bp.route('/new_password', methods=['POST'])
@auth_required
@swag_from('yaml/new_password.yaml')
def new_password_():
	req = request.get_json(force=True)
	old_password = req.get('old_password', None)
	new_password = req.get('new_password', None)
	from app.service.auth.my_profile.settings.route_handlers import\
		new_password_s
	new_password_s(current_user(), old_password, new_password)
	return Response(status=200)


@bp.route('/new_email', methods=['POST'])
@auth_required
@swag_from('yaml/new_email.yaml')
def new_email_():
	req = request.get_json(force=True)
	new_email = req.get('new_email', None)
	from app.service.auth.my_profile.settings.route_handlers import\
		new_email_s
	new_email_s(current_user(), new_email)
	return Response(status=200)


@bp.route('/new_login', methods=['POST'])
@auth_required
@swag_from('yaml/new_login.yaml')
def new_login_():
	req = request.get_json(force=True)
	new_login = req.get('new_login', None)
	from app.service.auth.my_profile.settings.route_handlers import \
		new_login_s
	new_login_s(current_user(), new_login)
	return Response(status=200)


@bp.route('/new_username', methods=['POST'])
@auth_required
@swag_from('yaml/new_username.yaml')
def new_username_():
	req = request.get_json(force=True)
	new_username = req.get('new_username', None)
	from app.service.auth.my_profile.settings.route_handlers import\
		new_username_s
	new_username_s(current_user(), new_username)
	return Response(status=200)


@bp.route('/new_phone', methods=['POST'])
@auth_required
@swag_from('yaml/new_phone.yaml')
def new_phone_():
	req = request.get_json(force=True)
	new_phone = req.get('new_phone', None)
	from app.service.auth.my_profile.settings.route_handlers import \
		new_phone_s
	new_phone_s(current_user(), new_phone)
	return Response(status=200)


@bp.route('/confirm/<token>', methods=['POST'])
@swag_from('yaml/confirm_email.yaml')
def confirm_email(token):
	from app.service.auth.my_profile.settings.route_handlers import\
		confirm_email_s
	confirm_email_s(token)
	return Response(status=202)
