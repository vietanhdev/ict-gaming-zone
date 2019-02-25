from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('USERS', description='User related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='User email address'),
        'username': fields.String(required=True, description='User username'),
        'password': fields.String(required=True, description='User password'),
        'public_id': fields.String(description='User Identifier')
    })


class AuthDto:
    api = Namespace('AUTH', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
