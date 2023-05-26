from app import db, guard
from app.api.auth.email import send_password_reset_email,\
	send_signup_confirm_email
from app.api.auth.validators import email_validate, password_validate,\
	phone_validate
from app.errors.handlers import ElementNotFoundError, JSONNotEnoughError,\
	ValidationError,\
	WrongTokenError
from app.helpers.functions import none_check
from app.models.user import User
from app.models.user_signup import UserSignup


def login_s(login, password):
	if None in [login, password]:
		raise JSONNotEnoughError()
	us = User.lookup(login)
	if us:
		password = us.hashed_password(password)
	user = guard.authenticate(login, password)
	return guard.encode_jwt_token(user)


def signup_s(login, email, name, phone, password):
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
	return user


def signup_confirm_s(token):
	if UserSignup.verify_confirmation_email_token(token) is None:
		raise WrongTokenError()
	db.session.commit()


def reset_password_request_s(email):
	if email is None:
		raise JSONNotEnoughError()
	user = User.search_by_email(email)
	if user is None:
		raise ElementNotFoundError()
	send_password_reset_email(user)

def reset_password_s(token,password):
	user = User.verify_reset_password_token(token)
	if user is None:
		raise WrongTokenError()
	if password is None:
		raise JSONNotEnoughError()
	if not password_validate(password):
		raise ValidationError()
	if password:
		user.set_password(password)
		return 200
	return 404