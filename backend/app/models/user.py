from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
from secrets import token_hex
from time import time

import jwt
from flask import current_app

from app import db, guard
from app.errors.handlers import ValidationError
from app.helpers.functions import none_check


@dataclass
class User(db.Model):
	__tablename__ = 'USER'
	user_id: int
	user_login: str
	# user_password: str
	user_name: str
	user_email: str
	user_phone: str
	user_money: int
	user_roles: str
	user_isactive: int
	# user_datetime: datetime
	items: str

	serialize_rules = ('-items.user',)

	user_id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
	user_login = db.Column(db.String(150), unique=True, index=True)
	user_password = db.Column(db.String(128))
	user_name = db.Column(db.String(120), index=True)
	user_email = db.Column(db.String(120), unique=True, index=True)
	user_phone = db.Column(db.String(9), default='', index=True)
	user_money = db.Column(db.Integer, default=0)
	user_roles = db.Column(db.Text, default='')
	user_isactive = db.Column(db.Integer, default=1, server_default='',
	                          index=True)
	user_datetime = db.Column(db.DateTime, default=datetime.utcnow,
	                          index=True)

	@property
	def items(self):
		from app.models.item import Item
		from app.models.item_in_use import ItemInUse
		return ItemInUse.query.join(
			Item, ItemInUse.item_id == Item.item_id).filter(
			ItemInUse.user_id == self.user_id).order_by(
			ItemInUse.use_datetime.desc()).all()

	@property
	def identity(self):
		return self.user_id

	@property
	def rolenames(self):
		"""
		*Required
		Attribute or Property *

		flask - praetorian
		requires
		that
		the
		user

		class has a ``rolenames`` instance

		attribute or property
		that
		provides
		a
		list
		of
		strings
		that
		describe
		the
		roles
		attached
		to
		the
		user
		instance
		"""
		try:
			return self.user_roles.split(',')
		except Exception:
			return []

	@property
	def password(self):
		"""
		*Required
		Attribute or Property *

		flask - praetorian
		requires
		that
		the
		user

		class has a ``password`` instance

		attribute or property
		that
		provides
		the
		hashed
		password
		assigned
		to
		the
		user
		instance
		"""
		return self.user_password

	@classmethod
	def lookup(cls, username):
		"""
		*Required
		Method *

		flask - praetorian
		requires
		that
		the
		user

		class implements a ``lookup()``

		class method that takes a single ``username`` argument and returns a
		user

		instance if there is one
		that
		matches or ``None`` if there is not.
		"""
		return cls.query.filter_by(user_login=username).one_or_none()

	@classmethod
	def identify(cls, id):
		"""
		*Required
		Method *

		flask - praetorian
		requires
		that
		the
		user

		class implements an ``identify()``

		class method that takes a single ``id`` argument and returns user
		instance if

		there is one
		that
		matches or ``None`` if there is not.
		"""
		return cls.query.get(id)

	@staticmethod
	def verify_settings_email_token(token):
		try:
			data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'],
			                  algorithms=['HS256'])
			user = User.search_by_id(data['confirm_email'])
			email = data['email']
			user.set_email(email)
			return True
		except:
			return None

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['JWT_SECRET_KEY'],
			                algorithms=['HS256'])[
				'reset_password']
		except:
			return None
		return User.query.get(id)

	@staticmethod
	def search_by_login(login):
		return User.query.filter_by(user_login=login).first()

	@staticmethod
	def search_by_phone(phone):
		return User.query.filter_by(user_phone=phone).first()

	@staticmethod
	def search_by_email(email):
		return User.query.filter_by(user_email=email).first()

	@staticmethod
	def search_by_id(id):
		return User.query.filter_by(user_id=id).first()

	def is_valid(self):
		return self.user_isactive

	def add_salt(self):
		from app.models.user_salt import UserSalt

		salt = UserSalt(user_id=self.user_id, salt=token_hex(64))
		db.session.add(salt)
		db.session.commit()

	def add(self):
		from app.models.user_signup import UserSignup

		if not none_check(6, [self.search_by_phone(
				self.user_phone),
			self.search_by_login(self.user_login),
			self.search_by_email(
				self.user_email), UserSignup.search_by_email(
				self.user_email), UserSignup.search_by_login(self.user_login),
			UserSignup.search_by_phone(self.user_phone)]):
			raise ValidationError("Phone, email and login must be valid.")
		db.session.add(self)
		a_user = User.search_by_login(self.user_login)
		self.add_salt()
		self.set_password(a_user.user_password)
		db.session.commit()

	def delete(self):
		from app.models.item_in_use import ItemInUse
		from app.models.user_salt import UserSalt

		salt = UserSalt.search_by_id(self.user_id)
		items = ItemInUse.search_by_user(self.user_id)
		for x in items:
			x.delete()
		db.session.delete(self)
		db.session.delete(salt)
		db.session.commit()

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.user_id, 'exp': time() + expires_in},
			current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

	def get_settings_confirm_email_token(self, email, expires_in=24 * 60 *
	                                                             60):
		return jwt.encode({
			'confirm_email': self.user_id,
			'exp':           time() + expires_in,
			'email':         email
			}, current_app.config['JWT_SECRET_KEY'],
			algorithm='HS256')

	def set_password(self, password):
		self.user_password = guard.hash_password(
			self.hashed_password(password))
		db.session.commit()

	def set_login(self, login):
		self.user_login = login
		db.session.commit()

	def set_username(self, username):
		self.user_name = username
		db.session.commit()

	def set_phone(self, phone):
		self.user_phone = phone
		db.session.commit()

	def set_email(self, email):
		self.user_email = email
		db.session.commit()

	def hashed_password(self, password):
		from app.models.user_salt import UserSalt

		salt = UserSalt.query.filter_by(user_id=self.user_id).first().salt
		return md5(password.encode()).hexdigest() + salt
