from flask_restplus import Namespace, fields

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


class UserDto:
    api = Namespace('USERS', description='User related operations', authorizations=authorizations, security='apikey')
    user_result = api.model('user', {
        'status': fields.String(required=False, description='Request status', default='success'),
        'message': fields.String(required=False, description='Response message to user',  default=''),
        'name': fields.String(required=False, description='User display name'),
        'email': fields.String(required=False, description='User email address'),
        'username': fields.String(required=False, description='User username'),
        'password': fields.String(required=False, description='User password'),
        'public_id': fields.String(description='User Identifier')
    })
    non_public_id_user = api.model('non_public_id_user', {
        'name': fields.String(required=True, description='User display name'),
        'email': fields.String(required=True, description='User email address'),
        'username': fields.String(required=True, description='User username'),
        'password': fields.String(required=True, description='User password'),
    })


class AuthDto:
    api = Namespace('AUTH', description='Authentication related operations', authorizations=authorizations, security='apikey')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
