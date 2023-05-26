from flask import jsonify


def my_data_s(user):
	return jsonify(user=user)


def my_roles_s(user):
	return jsonify(roles=list(user.rolenames))
