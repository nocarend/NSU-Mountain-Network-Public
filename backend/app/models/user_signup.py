from dataclasses import dataclass
from datetime import datetime
from time import time

import jwt
from flask import current_app

from app import db
from app.errors.handlers import ValidationError
from app.helpers.functions import none_check


@dataclass
class UserSignup(db.Model):
	__tablename__ = 'USER_SIGNUP'
	signup_id: int
	user_login: str
	# user_password: str
	user_name: str
	user_email: str
	user_phone: str
	signup_datetime: datetime

	signup_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	user_login = db.Column(db.String(150), unique=True, index=True)
	user_password = db.Column(db.String(128))
	user_name = db.Column(db.String(120), index=True)
	user_email = db.Column(db.String(120), unique=True, index=True)
	user_phone = db.Column(db.String(9), unique=True, index=True)
	signup_datetime = db.Column(db.DateTime, default=datetime.utcnow, index=True)

	@staticmethod
	def search_by_id(id):
		return UserSignup.query.filter_by(signup_id=id).first()

	@staticmethod
	def search_by_login(login):
		return UserSignup.query.filter_by(user_login=login).first()

	@staticmethod
	def search_by_email(email):
		return UserSignup.query.filter_by(user_email=email).first()

	@staticmethod
	def search_by_phone(phone):
		return UserSignup.query.filter_by(user_phone=phone).first()

	@staticmethod
	def verify_confirmation_email_token(token):
		try:
			data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
			user = UserSignup(user_login=data['login'], user_password=data['password'],
			                  user_name=data['name'], user_email=data['email'], user_phone=data[
					'phone'])
			user.add()
			return True
		except:
			return None

	def add(self):
		from app.models.user import User

		if not none_check(2, [User.search_by_email(self.user_email), self.search_by_email(
				self.user_email)]):
			raise ValidationError()
		db.session.add(self)
		db.session.commit()

	def add_user(self):
		from app.models.user import User

		user = User(user_login=self.user_login, user_password=self.user_password,
		            user_name=self.user_name, user_email=self.user_email,
		            user_phone=self.user_phone)
		db.session.add(user)
		db.session.commit()
		a_user = User.search_by_login(self.user_login)
		a_user.add_salt()
		a_user.set_password(self.user_password)
		self.delete()
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def get_confirmation_token(self, expires_in=60 * 60 * 24 * 7):
		return jwt.encode({
			'login': self.user_login, 'password': self.user_password,
			'name':  self.user_name,
			'email': self.user_email, 'phone': self.user_phone, 'exp': time() + expires_in
			},
			current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
