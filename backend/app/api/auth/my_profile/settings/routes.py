from flask import request, Response
from flask_praetorian import auth_required, current_user

from app import guard
from app.api.auth.validators import email_validate, login_validate,\
	password_validate, phone_validate
from app.errors.handlers import JSONNotEnoughError, ValidationError
from app.models.user import User
from . import bp
from ...email import send_settings_confirm_email


@bp.route('/new_password', methods=['POST'])
@auth_required
def new_password():
	req = request.get_json(force=True)
	old_password = req.get('old_password', None)
	new_password = req.get('new_password', None)
	if None in [old_password, new_password]:
		raise JSONNotEnoughError()
	if not password_validate(new_password):
		raise ValidationError("New password should be more than 5 symbols.")
	user = guard.authenticate(current_user().user_login,
	                          current_user().hashed_password(
		                          old_password))
	user.set_password(new_password)
	return Response(status=200)


# сделать confirm для нового емайла
@bp.route('/new_email', methods=['POST'])
@auth_required
def new_email():
	req = request.get_json(force=True)
	new_email = req.get('new_email', None)
	if new_email is None:
		raise JSONNotEnoughError()
	if not email_validate(new_email) or User.search_by_email(
			new_email) is not None:
		raise ValidationError("Email is wrong!")
	send_settings_confirm_email(current_user(), new_email)
	return Response(status=200)


@bp.route('/new_login', methods=['POST'])
@auth_required
def new_login():
	req = request.get_json(force=True)
	new_login = req.get('new_login', None)
	if new_email is None:
		raise JSONNotEnoughError()
	if not login_validate(new_login) or User.search_by_login(
			new_login) is not None:
		raise ValidationError(
			"New login should be more than 5 symbols and be unique.")
	user = current_user()
	user.set_login(new_login)
	return Response(status=200)


@bp.route('/new_username', methods=['POST'])
@auth_required
def new_username():
	req = request.get_json(force=True)
	new_username = req.get('new_username', None)
	if new_username is None:
		raise JSONNotEnoughError()
	user = current_user()
	user.set_username(new_username)
	return Response(status=200)


@bp.route('/new_phone', methods=['POST'])
@auth_required
def new_phone():
	req = request.get_json(force=True)
	new_phone = req.get('new_phone', None)
	if new_phone is None:
		raise JSONNotEnoughError()
	if phone_validate(new_phone) or User.search_by_phone(
			new_phone) is not None:
		raise ValidationError(
			"Number's format is wrong or phone is already taken.")
	user = current_user()
	user.set_phone(new_phone)
	return Response(status=200)
