from flask import request, g
from flask_restplus import Resource, fields
from flask_babel import gettext, ngettext

from app.main.utils.decorator import admin_token_required, token_required
from app.main.utils.dto import UserDto
from app.main.user.services.user_service import save_new_user, get_all_users, get_user, update_user

api = UserDto.api
user_result = UserDto.user_result
non_public_id_user = UserDto.non_public_id_user


@api.route('/')
class UserList(Resource):

    @api.doc('List of registered users')
    # @admin_token_required
    @api.marshal_list_with(user_result, envelope='data')
    @api.doc(security='apikey')
    def get(self):
        """List all registered users"""
        return get_all_users()

    
    @api.doc('Create a new user')
    @api.expect(non_public_id_user, validate=True)
    @api.response(201, gettext(u'User successfully created'))
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, gettext(u'User not found.'))
class User(Resource):
    @api.doc('Get a user')
    @api.marshal_with(user_result)
    @token_required
    @api.doc(security='apikey')
    def get(self, public_id):
        """get a user given its identifier"""

        # Get user from @token_required
        user = g.user

        # IMPORTANT: Check to ensure that only user can malipulate their account
        if user.get('public_id') != public_id:
            return {
                'status': 'fail',
                'message': gettext(u'Permission Denied.')
            }, 403

        user = get_user(user.get('user_id'))
        if not user:
            api.abort(404)
        else:
            return user


    new_user_details = api.model('new_user_details', {
        'email': fields.String(required=False, description='New user email address'),
        'old_password': fields.String(required=False, description='Old user password. This field if neccessary when user wants to change password.'),
        'password': fields.String(required=False, description='New user password. This field if neccessary when user wants to change password.'),
    })
    @api.doc('Update a user')
    @token_required
    @api.expect(new_user_details)
    @api.param('public_id', 'The User identifier')
    @token_required
    @api.doc(security='apikey')
    def put(self, public_id):
        """Update user details """

        # Get user from @token_required
        user = g.user

        # IMPORTANT: Check to ensure that only user can malipulate their account
        if user.get('public_id') != public_id:
            return {
                'status': 'fail',
                'message': gettext(u'Permission Denied.')
            }, 403

        data = request.json
        data["user_id"] = user.get('user_id')
        return update_user(data=data)



