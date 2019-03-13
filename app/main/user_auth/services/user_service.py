import uuid
import datetime
import re

from flask import request
from app.main import db
from app.main.user_auth.models.user_model import User
from flask_babel import gettext, ngettext
from .auth_service import Auth

def get_users():
    return User.query.all()

def get_user(id):
    return User.query.filter_by(id=id).first()

def update_user(data):
    try:
        user = User.query.filter_by(id=data['id']).first()

        if not user:
            response_object = {
                'status': 'fail',
                'message': gettext(u'User not found.'),
            }
            return response_object, 404


        # User wants to update name
        if 'name' in data.keys():
            if 3 > len(data['name']) or len(data['name']) > 50:
                return {
                    'status': 'fail',
                    'error_code': 4002,
                    'message': gettext(u'Ensure that you specified a name having 3-50 characters.'),
                }, 400
            else:
                user.name = data['name']

        # User wants to update email
        if 'email' in data.keys():

            #  Check Email format
            if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data['email']):
                response_object = {
                    'status': 'fail',
                    'message': gettext(u'Invalid email address.'),
                }

            if 3 > len(data['email']) or len(data['email']) > 50:
                return {
                    'status': 'fail',
                    'error_code': 4003,
                    'message': gettext(u'Ensure that you specified a correct email having 3-50 characters.')
                }, 400

            # Check email existence
            same_mail_user = User.query.filter_by(email=data['email']).first()
            if same_mail_user:
                return {
                    'status': 'fail',
                    'message': gettext(u'Email already exists. Please choose another.'),
                }, 409

            user.email = data['email']

        # User wants to change the password
        if 'old_password' in data.keys() and 'password' in data.keys():

            # Check old password
            if not user.check_password(data.get('old_password')):
                response_object = {
                    'status': 'fail',
                    'message': gettext(u'Wrong old password.')
                }
                return response_object, 403

            # Check password characters and ensure it having at least 1 number
            if not ( re.match(r'[A-Za-z0-9@#$%^&+=]{5,10}', data.get('password')) and any(c.isdigit() for c in data.get('password')) ):
                return {
                    'status': 'fail',
                    'error_code': 4005,
                    'message': gettext(u'Wrong password format. Please use a password from 5-10 characters, containing only A-Z a-z 0-9 and special characters (@ # $ % ^ & + =). The password must have at least 1 number.')
                }, 400

            user.password = data.get('password')

        db.session.commit()
        response_object = {
            'status': 'success',
            'message': gettext(u'Updated successfully.')
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Could not update user.',
        }
        return response_object, 500



def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def create_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Check missing fields and field length

    if name is None or not (3 <= len(name) <= 50):
        return {
            'status': 'fail',
            'error_code': 4002,
            'message': gettext(u'Ensure that you specified a name having 3-50 characters.'),
        }, 400

    if email is None or not (3 <= len(name) <= 50):
        return {
            'status': 'fail',
            'error_code': 4003,
            'message': gettext(u'Ensure that you specified a correct email having 3-50 characters.')
        }, 400

    if password is None:
        return {
            'status': 'fail',
            'error_code': 4004,
            'message': gettext(u'Please specify password for user.'),
        }, 400

    # Check password characters and ensure it having at least 1 number
    if not ( re.match(r'[A-Za-z0-9@#$%^&+=]{5,10}', password) and any(c.isdigit() for c in password) ):
        return {
            'status': 'fail',
            'error_code': 4005,
            'message': gettext(u'Wrong password format. Please use a password from 5-10 characters, containing only A-Z a-z 0-9 and special characters (@ # $ % ^ & + =). The password must have at least 1 number.')
        }, 400

    #  Check Email format
    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
        response_object = {
            'status': 'fail',
            'error_code': 4003,
            'message': gettext(u'Invalid email address.'),
        }
        return response_object, 400

    # Check email existence
    user = User.query.filter_by(email=data['email']).first()
    if user:
        response_object = {
            'status': 'fail',
            'error_code': 4006,
            'message': gettext(u'Your email is already used for another account. Please use another one.'),
        }
        return response_object, 409

    # Generate public_id for user and check duplication in DB
    public_id = ''
    while True:
        public_id = str(uuid.uuid4())

        # Duplication check in DB
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            break

    new_user = User(
        public_id=public_id,
        name=data['name'],
        email=data['email'],
        password=data['password'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(new_user)
    return generate_token(new_user)

def generate_token(user):
    try:
        # generate the auth token
        auth_token = Auth.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': gettext(u'Successfully registered.'),
            'public_id': user.public_id,
            'token': auth_token.decode()
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'error_code': 500,
            'message': gettext(u'Server Internal Error.')
        }
        return response_object, 500

def save_changes(data):
    db.session.add(data)
    db.session.commit()

