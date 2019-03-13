from flask import request, g
from flask_restplus import Resource, fields, marshal
from flask_babel import gettext, ngettext

from app.main.user_auth.utils.request_verify import require_json_request

from .utils.dto import UserDto
from .services.user import create_user, get_users, get_user, update_user

from .utils.decorator import admin_token_required, user_token_required

# Load api namespace
api = UserDto.api

@api.route('/')
class UserList(Resource):

    @api.doc('List of users')
    @admin_token_required
    @api.doc(security='apikey')
    def get(self):
        """List all registered users"""
        data = marshal(get_users(), UserDto.user_details)
        return {
            'status': 'success',
            'data': data
        }

    @api.doc('Register a new user')
    @api.expect(UserDto.new_user_details, validate=False)
    @require_json_request
    def post(self):
        """Creates a new user """
        data = request.get_json()
        return create_user(data=data)


@api.route('/<public_id>/')
@api.param('public_id', 'The User identifier')
@api.response(404, gettext(u'User not found.'))
class User(Resource):
    @api.doc('Get a user')
    @user_token_required
    @api.doc(security='apikey')
    def get(self, public_id):
        """get a user given its identifier"""

        user = g.user

        # IMPORTANT: Check to ensure that only user can malipulate their account
        if user.get('public_id') != public_id:
            return {
                'status': 'fail',
                'message': gettext(u'Permission Denied.')
            }, 403

        user = get_user(user.get('id'))
        
        if not user:
            return {
                'status': 'fail',
                'message': gettext(u'User Not Found.')
            }, 404
        else:
            return {
                'status': 'success',
                'data': marshal(user, UserDto.user_details)
            }

    @api.doc('Update a user')
    @user_token_required
    @api.expect(UserDto.new_user_details)
    @api.param('public_id', 'The User identifier')
    @api.doc(security='apikey')
    def put(self, public_id):
        """Update user details """

        user = g.user

        # IMPORTANT: Check to ensure that only user can malipulate their account
        if user.get('public_id') != public_id:
            return {
                'status': 'fail',
                'message': gettext(u'Permission Denied.')
            }, 403

        data = request.json
        data['id'] = user.get('id')
        return update_user(data=data)

    
