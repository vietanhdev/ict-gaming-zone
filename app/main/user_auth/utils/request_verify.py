from functools import wraps
from flask import request, jsonify
from flask_babel import gettext, ngettext

def require_json_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            post_data = request.get_json(force=True)
        except Exception:
            return {
                'status': 'fail',
                'message': gettext(u'Request is invalid. Please use JSON format.'),
                'error_code': 4001
            }, 400;
        return f(*args, **kwargs)
    return decorated
