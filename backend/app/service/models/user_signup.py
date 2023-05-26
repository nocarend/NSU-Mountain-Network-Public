from flask import jsonify

from app import db
from app.models.user_signup import UserSignup


def signup_requests_get_s():
	return jsonify(requests=UserSignup.getAll())


def approve_user_s(signup_id):
	user = UserSignup.search_by_id(signup_id)
	if user:
		user.add_user()
		db.session.commit()
	return user

def reject_user_s(signup_id):
	user = UserSignup.search_by_id(signup_id)
	if user:
		user.delete()
		db.session.commit()
	return user