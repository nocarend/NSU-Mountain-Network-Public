from datetime import timedelta

import jwt
import redis
from flask import current_app
from flask_praetorian.exceptions import BlacklistedError

delta = timedelta(days=1)
# token_user_blacklist = redis.StrictRedis(
# 	host="redis", port=6379, db=0, decode_responses=True
# 	)
token_user_blacklist = set()


def to_user_blacklist(jti):
	token_user_blacklist.add(jti)
	# token_user_blacklist.set(jti, "", ex=delta)


def is_user_blacklisted(jti):
	return jti in token_user_blacklist
	# return token_user_blacklist.get(jti) is not None


def other_black_data(data):
	jti = data['jti']
	if is_other_blacklisted(jti):
		raise BlacklistedError()
	to_other_blacklist(jti)


if __name__ == '__main__':
	other_black_data({'jti': '1'})


def to_other_blacklist(jti):
	token_user_blacklist.add(jti)
	# token_user_blacklist.set(jti, "", ex=delta)


def is_other_blacklisted(jti):
	return jti in token_user_blacklist
	# return token_user_blacklist.get(jti) is not None


def to_jti(data):
	return jwt.encode({'jti': data}, current_app.config['SECRET_KEY'],
	                  algorithm='HS512')
