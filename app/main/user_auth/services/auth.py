from flask_babel import gettext, ngettext
import jwt
import datetime
from flask import current_app as app
from app.main.user_auth.models.blacklist_token import BlacklistToken
from app.main.user_auth.services.blacklist import save_token

from app.main.user_auth.models.user import User

class Auth:

    @staticmethod
    def get_secret_key():
        return app.config['SECRET_KEY']

    @staticmethod
    def get_admin_username():
        return app.config['ADMIN_USERNAME']

    @staticmethod
    def get_admin_password():
        return app.config['ADMIN_PASSWORD']

    @staticmethod
    def login_admin(data):
        """
        Process an admin login
        """
        try:
            username = data.get('username');
            password = data.get('password');

            if (Auth.get_admin_username() != username or
                Auth.get_admin_password() != password
            ):
                return {
                    'status': 'fail',
                    'error_code': 4031,
                    'message': gettext(u'Email or password does not match.')
                }, 403

            else:
                auth_token = Auth.encode_auth_token(Auth.get_admin_username());

                return {
                    'status': 'success',
                    'message': gettext(u'Successfully logged in.'),
                    'token': auth_token.decode()
                }, 200

        
        except Exception as e:
            print(e);
            return {
                'status': 'fail',
                'error_code': 500,
                'message': gettext(u'Internal Server Error.')
            }, 500


    @staticmethod
    def login_user(data):
        """
        Process a user login
        """
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = Auth.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': gettext(u'Successfully logged in.'),
                        'token': auth_token.decode(),
                        'user': {
                            "name": user.name,
                            "email": user.email,
                            "public_id": user.public_id
                        }
                    }
                    return response_object, 200
            else:
                return {
                    'status': 'fail',
                    'error_code': 4031,
                    'message': gettext(u'Email or password does not match.')
                }, 403

        except Exception as e:
            print(e);
            return {
                'status': 'fail',
                'error_code': 500,
                'message': gettext(u'Internal Server Error.')
            }, 500


    @staticmethod
    def check_admin_token(admin_token):
        resp = Auth.decode_auth_token(admin_token)
        if (resp.get('status') == 'fail'):
            return resp
        else:
            resp['is_admin'] = (resp.get('sub') == Auth.get_admin_username())
            return resp

    @staticmethod
    def check_user_token(bearer_token):
        resp = Auth.decode_auth_token(bearer_token)
        if (resp.get('status') == 'fail'):
            return resp
        else:
            resp['is_admin'] = (resp.get('sub') == Auth.get_admin_username())
            return resp
            
    @staticmethod
    def logout(bearer_token):
        resp = Auth.decode_auth_token(bearer_token)
        if resp.get('status') == 'success':
            # mark the token as blacklisted
            auth_token = bearer_token.split()[1]
            return save_token(token=auth_token)
        else:
            return resp, 403

    @staticmethod
    def encode_auth_token(subject):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': subject
            }
            return jwt.encode(
                payload,
                Auth.get_secret_key(),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        # Remove Bearer part
        try:
            auth_token = auth_token.split()[1]
        except Exception:
            return {
                    'status': 'fail',
                    'error_code': 4034, 
                    'message': gettext(u'Invalid token.')
                } 
        try:
            payload = jwt.decode(auth_token, Auth.get_secret_key())
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return {
                    'status': 'fail',
                    'error_code': 4032, 
                    'message': gettext(u'Token blacklisted. Please log in again.')
                }  
            else:
                return {
                    'status': 'success',
                    'sub': payload['sub']
                } 
        except jwt.ExpiredSignatureError:
            return {
                    'status': 'fail',
                    'error_code': 4033, 
                    'message': gettext(u'Signature expired. Please log in again.')
                } 
        except jwt.InvalidTokenError:
            return {
                    'status': 'fail',
                    'error_code': 4034, 
                    'message': gettext(u'Invalid token.')
                } 