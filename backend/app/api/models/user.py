from flasgger import swag_from
from flask import jsonify, request, Response
from flask_praetorian import current_rolenames, current_user, roles_accepted

from app import db
from app.api.auth.validators import email_validate, password_validate,\
	phone_validate
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError,\
	MethodNotAllowedError,\
	StockError, ValidationError
from app.helpers.functions import get_user_data, none_check
from app.models.user import User
from app.models.user_signup import UserSignup
from . import bp
from ...models.money_history import MoneyHistory


@bp.route('/users', methods=['GET'])
@roles_accepted('treasurer', 'warehouseman', 'admin')
@swag_from('yaml/user/users_get.yaml')
def users_get():
	return jsonify(
		users=list({'user': user} for user in User.query.all())), 200


@bp.route('/users', methods=['POST'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/user/users_post.yaml')
def users_post():
	req = request.get_json(force=True)
	login, password, name, email, phone = get_user_data(req)
	if None in [login, password, name, email, phone]:
		raise JSONNotEnoughError()
	if not email_validate(email) or not phone_validate(
			phone) or not password_validate(
		password):
		raise ValidationError()
	newUser = User(user_login=login, user_password=password, user_name=name,
	               user_email=email,
	               user_phone=phone)
	newUser.add()
	return Response(status=201)


@bp.route('/users/<username>', methods=['GET'])
@roles_accepted('treasurer', 'warehouseman', 'admin')
@swag_from('yaml/user/users_username_get.yaml')
def users_username_get(username):
	user = User.search_by_login(username)
	if user is None:
		raise ElementNotFoundError()
	return jsonify(user=user), 200


@bp.route('/users/<username>', methods=['DELETE'])
@roles_accepted('warehouseman', 'admin')
@swag_from('yaml/user/users_username_delete.yaml')
def users_username_delete(username):
	user = User.search_by_login(username)
	if user is None:
		raise ElementNotFoundError()
	for i in user.items:
		if i.is_confirm != 5:
			raise StockError()
	# protected_from_treasurer()
	user.delete()
	return Response(status=204)


@bp.route('/users/<username>', methods=['PATCH'])
@roles_accepted('treasurer', 'warehouseman', 'admin')
@swag_from('yaml/user/users_username_patch.yaml')
def users_username_patch(username):
	user = User.search_by_login(username)
	req = request.get_json(force=True)
	req = req.get('user', None)
	if user is None:
		raise ElementNotFoundError()
	money = req.get('money', user.user_money)
	if user.user_money != money:
		MoneyHistory.add(user.user_id, current_user().user_id,
		                 user.user_money,
		                 money)
		user.user_money = money
	if 'admin' in current_rolenames() or 'warehouseman' in\
			current_rolenames():
		login, password, name, email, phone = get_user_data(req)
		roles = req.get('roles', user.user_roles)
		is_active = req.get('is_active', user.user_isactive)
		if not none_check(6, [User.search_by_phone(phone) if phone else
		                      None,
		                      User.search_by_email(email) if email else
		                      None,
		                      User.search_by_login(
			                      login) if login else None,
		                      UserSignup.search_by_login(login) if login
		                      else None,
		                      UserSignup.search_by_email(email) if email
		                      else None,
		                      UserSignup.search_by_phone(phone) if phone
		                      else None]):
			raise ValidationError()
		if 'admin' not in current_rolenames() and 'admin' in\
				User.search_by_login(\
						login).rolenames():
			raise MethodNotAllowedError()
		if login:
			user.user_login = login
		if name:
			user.user_name = name
		if password:
			user.set_password(password)
		if email:
			user.user_email = email
		if phone:
			user.user_phone = phone
		user.user_roles = roles
		user.user_isactive = is_active
	db.session.commit()
	return Response(status=200)
