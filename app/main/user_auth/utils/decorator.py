from functools import wraps
from flask import request, g
from app.main.user_auth.services.auth import Auth
from flask_babel import gettext, ngettext
from app.main.user_auth.services.user import get_user_by_id

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # get the auth token
        try:
            auth_token = request.headers.get('Authorization')
        except Exception:
            return  {
                'status': 'fail',
                'error_code': 4035,
                'message': gettext(u'Please provide a valid auth token.')
            }, 403


        admin_check_resp = Auth.check_admin_token(auth_token)

        if (admin_check_resp.get('status') == 'fail'):
            return admin_check_resp
        elif not admin_check_resp['is_admin']:
            return {
                'status': 'fail',
                'error_code': 4036,
                'message': gettext(u'Admin token required')
            }, 403

        return f(*args, **kwargs)

    return decorated


def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # get the auth token
        try:
            bearer_token = request.headers.get('Authorization')
        except Exception:
            return  {
                'status': 'fail',
                'error_code': 4035,
                'message': gettext(u'Please provide a valid auth token.')
            }, 403


        user_check_resp = Auth.check_user_token(bearer_token)

        # If token is invalid
        if (user_check_resp.get('status') == 'fail'):
            return user_check_resp
            
        # Otherwise, check user public_id
        user_id = user_check_resp['sub']
        user_data = get_user_by_id(user_id);

        # Could not find a user with user id
        if not user_data:
            return  {
                'status': 'fail',
                'error_code': 4034,
                'message': gettext(u'Invalid token.')
            }, 403

        user = {}
        user['id'] = user_data.id
        user['email'] = user_data.email
        user['name'] = user_data.name
        user['public_id'] = user_data.public_id

        g.user = user

        return f(*args, **kwargs)

    return decorated