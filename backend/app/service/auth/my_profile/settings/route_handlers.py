from app import db, guard
from app.api.auth.email import send_settings_confirm_email
from app.api.auth.validators import email_validate, login_validate,\
	password_validate, phone_validate
from app.errors.handlers import JSONNotEnoughError, ValidationError,\
	WrongTokenError
from app.models.user import User


def new_password_s(user, old_password, new_password):
	if None in [old_password, new_password]:
		raise JSONNotEnoughError()
	if not password_validate(new_password):
		raise ValidationError("New password should be more than 5 symbols.")
	user = guard.authenticate(user.user_login,
	                          user.hashed_password(
		                          old_password))
	# AuthError
	user.set_password(new_password)
	db.session.commit()


def new_email_s(user, new_email):
	if new_email is None:
		raise JSONNotEnoughError()
	if not email_validate(new_email) or User.search_by_email(
			new_email) is not None:
		raise ValidationError("Email is wrong!")
	return send_settings_confirm_email(user, new_email)


def new_login_s(user, new_login):
	if new_login is None:
		raise JSONNotEnoughError()
	if not login_validate(new_login) or User.search_by_login(
			new_login) is not None:
		raise ValidationError(
			"New login should be more than 5 symbols and be unique.")
	user.set_login(new_login)
	db.session.commit()


def new_username_s(user, new_username):
	if new_username is None:
		raise JSONNotEnoughError()
	user.set_username(new_username)
	db.session.commit()


def new_phone_s(user, new_phone):
	if new_phone is None:
		raise JSONNotEnoughError()
	if not phone_validate(new_phone) or User.search_by_phone(
			new_phone) is not None:
		raise ValidationError(
			"Number's format is wrong or phone is already taken.")
	user.set_phone(new_phone)
	db.session.commit()

def confirm_email_s(token):
	if User.verify_settings_email_token(token) is None:
		raise WrongTokenError()
	db.session.commit()