from flasgger import swag_from
from flask_praetorian import auth_required, current_user

from app.service.auth.my_profile.route_handlers import my_data_s, my_roles_s
from . import bp


@bp.route('/', methods=['GET'])
@auth_required
@swag_from('yaml/my_data.yaml')
def my_data():
	return my_data_s(current_user())


@bp.route("/roles")
@auth_required
@swag_from('yaml/my_roles.yaml')
def my_roles():

	return my_roles_s(current_user())
