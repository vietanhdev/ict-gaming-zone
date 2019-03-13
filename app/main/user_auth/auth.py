from flask import request, jsonify
from flask_restplus import Resource

from .utils.dto import AuthDto
from .services.auth import Auth

from app.main.user_auth.utils.request_verify import require_json_request

# Load api namespace
api = AuthDto.api

@api.route('/admin/login')
class AdminLogin(Resource):
    """
        Admin Login Resource
    """
    @api.doc('This endpoint is for admin to login')
    @api.expect(AuthDto.admin_login_details)
    @require_json_request
    def post(self):
        post_data = request.get_json(force=True)
        return Auth.login_admin(data=post_data)


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('This endpoint is for users (users, students) to login')
    @api.expect(AuthDto.user_login_details)
    @require_json_request
    def post(self):
        post_data = request.get_json(force=True)
        return Auth.login_user(data=post_data)

@api.route('/logout')
class LogoutAPI(Resource):
    """
        Logout Resource
    """
    @api.doc('Logout a user')
    @api.doc(security='apikey')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization');
        return Auth.logout(bearer_token=auth_header)

