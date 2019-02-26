from app.main.user.models.user import User
from app.main.auth.services.blacklist_service import save_token
from flask_babel import gettext, ngettext

class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': gettext(u'Successfully logged in.'),
                        'Authorization': auth_token.decode(),
                        'user': {
                            "name": user.name,
                            "email": user.email,
                            "public_id": user.public_id
                        }
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': gettext(u'Email or password does not match.')
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': gettext(u'Try again.')
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data;
            # auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': gettext(u'Please provide a valid auth token.')
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'public_id': user.public_id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': gettext(u'Please provide a valid auth token.')
            }
            return response_object, 401
