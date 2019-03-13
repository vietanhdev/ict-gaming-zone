from functools import wraps

from flask import request, g

from app.main.user_auth.services.auth_helper import Auth

from flask_babel import gettext, ngettext

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        if status == 200 and data['status'] == 'success':
            g.user = data.get('data')

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': gettext(u'Admin token required')
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
