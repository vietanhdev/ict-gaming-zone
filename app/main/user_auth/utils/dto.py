from flask_restplus import Namespace, fields, marshal

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

class AuthDto:
    api = Namespace('AUTH', description='Authentication related operations', authorizations=authorizations, security='apikey')

    admin_login_details = api.model('admin_login_details', {
        'username': fields.String(required=True, description='The username of admin'),
        'password': fields.String(required=True, description='The admin password'),
    })

    user_login_details = api.model('user_login_details', {
        'email': fields.String(required=True, description='The user email'),
        'password': fields.String(required=True, description='The user password'),
    })

class UserDto:
    api = Namespace('USERS', description='User related operations', authorizations=authorizations, security='apikey')

    new_user_details = api.model('new_user_details', {
        'name': fields.String(required=True, description='The name of new user'),
        'email': fields.String(required=True, description='The email of new user'),
        'password': fields.String(required=True, description='The password of new user'),
    })

    user_details = api.model('user_details', {
        'name': fields.String(required=True, description='The name of user'),
        'email': fields.String(required=True, description='The email of user'),
        'public_id': fields.String(required=True, description='The public id of user')
    })