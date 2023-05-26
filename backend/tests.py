#!/usr/bin/env python
import unittest

import pytest
from flask import jsonify
from flask_praetorian.exceptions import AuthenticationError

from app import create_app, db, guard
from app.models.user import User
from app.models.user_signup import UserSignup
from app.service.auth.my_profile.route_handlers import my_data_s, my_roles_s
from app.service.auth.my_profile.settings.route_handlers import\
	confirm_email_s,\
	new_email_s,\
	new_login_s,\
	new_password_s, new_phone_s, new_username_s
from app.service.auth.route_handlers import signup_s
from app.service.models.user_signup import signup_requests_get_s
from config import Config


class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite://'


# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class AuthModelCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		u = User(user_login="susan", user_name='susan',
		         user_email="susan@yandex.ru",
		         user_password="cat")
		u.add()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_success_login(self):
		from app.service.auth.route_handlers import login_s
		user = login_s('susan', 'cat')
		self.assertIsNotNone(user)

	def test_fail_login(self):
		with pytest.raises(AuthenticationError):
			from app.service.auth.route_handlers import login_s
			login_s('horse_shit', 'cat')

	def test_signup(self):
		from app.service.auth.route_handlers import signup_s
		self.assertIsNotNone(
			signup_s("mine", "sss@sss.ry", "moine", "8005553535", "moinet"))


class AuthMyProfileSettingsModelCase(unittest.TestCase):
	user: User

	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		u = User(user_login="susan", user_name='susan',
		         user_email="susan@yandex.ru",
		         user_password="cat", user_phone='0987654321')
		u.add()
		us = User.search_by_login('susan')
		global user
		user = guard.authenticate('susan', us.hashed_password('cat'))

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_password_check_fail(self):
		global user
		with pytest.raises(AuthenticationError):
			new_password_s(user, 'catt', 'lololo')

	def test_new_password(self):
		global user
		new_password_s(user, 'cat', 'tatata')
		self.assertTrue(guard._verify_password(user.hashed_password('tatata'),
		                                       user.user_password))

	def test_new_login(self):
		global user
		new_login_s(user, 'sucker')
		self.assertEquals(user.user_login, 'sucker')

	def test_new_username(self):
		global user
		new_username_s(user, 'cocker')
		self.assertEquals(user.user_name, 'cocker')

	def test_new_phone(self):
		global user
		new_phone_s(user, '1234567890')
		self.assertEquals(user.user_phone, '1234567890')

	def test_new_email(self):
		global user
		token = new_email_s(user, 'cacaca@caca.caac')
		confirm_email_s(token)
		self.assertEquals(user.user_email, 'cacaca@caca.caac')


class AuthMyProfileModelCase(unittest.TestCase):
	user: User

	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		u = User(user_login="susan", user_name='susan',
		         user_email="susan@yandex.ru",
		         user_password="cat", user_phone='0987654321')
		u.add()
		us = User.search_by_login('susan')
		global user
		user = guard.authenticate('susan', us.hashed_password('cat'))

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_my_data(self):
		self.assertEquals(jsonify(user=user).data, my_data_s(user).data)

	def test_my_roles(self):
		user.user_roles += 'warehouseman'
		self.assertEquals(list(user.rolenames),
		                  my_roles_s(user).get_json(force=True)['roles'])


class ModelsUserSignupModelCase(unittest.TestCase):
	user: User

	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		signup_s("minera", "sss@sss.ry", "moine", "8005553535", "moinet")

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_signup_requests_get(self):
		self.assertEquals(jsonify(requests=UserSignup.getAll()).data,
		                  signup_requests_get_s().data)

# def test_approve_user(self):
# 	# нужен конфирм емайла
# 	# ids = UserSignup.getAll()
# 	# print(ids)
# 	# approve_user_s(1)
# 	self.assertIsNotNone(User.search_by_login("minera"))
#
# def test_reject_user(self):
# 	# тоже нуден коннфирм емайла
# 	pass


# class ModelsUserSignupTestCase(unittest.TestCase):
# 	def setUp(self):
# 		self.app = create_app(TestConfig)
# 		self.app_context = self.app.app_context()
# 		self.app_context.push()
# 		db.create_all()
# 		u = User(user_login="susan", user_name='susan',
# 		         user_email="susan@yandex.ru",
# 		         user_password="cat", user_phone='0987654321')
# 		g = User(user_login='warehou', user_name='warehou',
# 		         user_email="aaa@aaa.aaa", user_phone='1234567899',
# 		         user_password='warehou', user_roles='warehouseman')
# 		u.add()
# 		g.add()
# 		i = Item(item_name="aboba",)
#
# 	def tearDown(self):
# 		db.session.remove()
# 		db.drop_all()
# 		self.app_context.pop()


if __name__ == '__main__':
	unittest.main(verbosity=2)
