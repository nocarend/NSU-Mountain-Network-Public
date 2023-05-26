from flasgger import swag_from
from flask import jsonify, request, Response
from flask_praetorian import auth_required
from flask_praetorian.exceptions import BlacklistedError, ExpiredAccessError,\
	InvalidTokenHeader,\
	InvalidUserError,\
	MissingToken

from app import db, guard
from app.api.auth import bp
from app.api.auth.email import send_password_reset_email,\
	send_signup_confirm_email
from app.api.auth.my_profile.routes import my_roles
from app.api.auth.validators import email_validate, password_validate,\
	phone_validate
from app.errors.handlers import AlreadyAuthError, ElementNotFoundError,\
	JSONNotEnoughError,\
	ValidationError,\
	WrongTokenError
from app.helpers.functions import none_check
from app.models.user import User
from app.models.user_signup import UserSignup
from app.tokens import to_user_blacklist


@bp.route('/signup', methods=['POST'])
@swag_from('yaml/routes/signup.yaml')
def signup():
	try:
		my_roles()
		raise AlreadyAuthError()
	except MissingToken:
		pass
	except InvalidTokenHeader:
		pass
	except ExpiredAccessError:
		pass
	except InvalidUserError:
		pass
	req = request.get_json(force=True)
	login = req.get('login', None)
	email = req.get('email', None)
	name = req.get('name', None)
	phone = req.get('phone', None)
	password = req.get('password', None)
	if None in [login, email, name, phone, password]:
		raise JSONNotEnoughError()
	if not email_validate(email) or not phone_validate(
			phone) or not password_validate(password):
		raise ValidationError()
	if not none_check(6, [UserSignup.search_by_login(login),
	                      UserSignup.search_by_email(
		                      email), UserSignup.search_by_phone(phone),
	                      User.search_by_email(email), User.search_by_login(
			login), User.search_by_phone(phone)]):
		raise ValidationError()
	user = UserSignup(user_login=login, user_name=name,
	                  user_email=email, user_phone=phone,
	                  user_password=password)
	send_signup_confirm_email(user)
	return Response(status=200)


@bp.route('/signup/confirm/<token>', methods=['POST'])
@swag_from('yaml/routes/signup_confirm.yaml')
def signup_confirm(token):
	try:
		my_roles()
		raise AlreadyAuthError()
	except MissingToken:
		pass
	except InvalidTokenHeader:
		pass
	except ExpiredAccessError:
		pass
	except InvalidUserError:
		pass
	except BlacklistedError:
		pass
	if UserSignup.verify_confirmation_email_token(token) is None:
		raise WrongTokenError()
	db.session.commit()
	return Response(status=200)


@bp.route('/login', methods=['POST'])
@swag_from('yaml/routes/login.yaml')
def login():
	try:
		my_roles()
		raise AlreadyAuthError()
	except MissingToken:
		pass
	except InvalidTokenHeader:
		pass
	except ExpiredAccessError:
		pass
	except InvalidUserError:
		pass
	except BlacklistedError:
		pass
	req = request.get_json(force=True)
	login = req.get('login', None)
	password = req.get('password', None)
	if None in [login, password]:
		raise JSONNotEnoughError()
	us = User.lookup(login)
	if us:
		password = us.hashed_password(password)
	user = guard.authenticate(login, password)
	return jsonify(access_token=guard.encode_jwt_token(user)), 200


@bp.route("/logout", methods=['POST'])
@auth_required
def logout():
	token = guard.extract_jwt_token(guard.read_token_from_header())
	to_user_blacklist(token['jti'])
	return Response(status=200)


@bp.route('/refresh', methods=['GET'])
@swag_from('yaml/routes/refresh.yaml')
def refresh():
	old_token = guard.read_token_from_header()
	to_user_blacklist(old_token)
	new_token = guard.refresh_jwt_token(old_token)
	return jsonify(access_token=new_token), 200


@bp.route('/reset_password_request', methods=['POST'])
@swag_from('yaml/routes/reset_password_request.yaml')
def reset_password_request():
	try:
		my_roles()
		raise AlreadyAuthError()
	except MissingToken:
		pass
	except InvalidTokenHeader:
		pass
	except ExpiredAccessError:
		pass
	except InvalidUserError:
		pass
	req = request.get_json(force=True)
	email = req.get('email', None)
	if email is None:
		raise JSONNotEnoughError()
	user = User.search_by_email(email)
	if user is None:
		raise ElementNotFoundError()
	send_password_reset_email(user)
	return Response(status=200)


@bp.route('/reset_password/<token>', methods=['POST'])
@swag_from('yaml/routes/reset_password.yaml')
def reset_password(token):
	try:
		my_roles()
		raise AlreadyAuthError()
	except MissingToken:
		pass
	except InvalidTokenHeader:
		pass
	except ExpiredAccessError:
		pass
	except InvalidUserError:
		pass
	user = User.verify_reset_password_token(token)
	if user is None:
		raise WrongTokenError()
	req = request.get_json(force=True)
	password = req.get('password', None)
	if password is None:
		raise JSONNotEnoughError()
	if not password_validate(password):
		raise ValidationError()
	if password:
		user.set_password(password)
	return Response(status=200 if password else 404)
