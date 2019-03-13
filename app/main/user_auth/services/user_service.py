import uuid
import datetime
import re

from flask import request
from app.main import db
from app.main.user_auth.models.user import User
from flask_babel import gettext, ngettext

def save_new_user(data):
    #  Check Email format
    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data['email']) is None:
        response_object = {
            'status': 'fail',
            'message': gettext(u'Invalid email address.'),
        }
        return response_object, 400

    # Check username format
    if re.match("^[A-Za-z0-9_-]*$", data['username']) is None or len(data['username']) == 0:
        response_object = {
            'status': 'fail',
            'message': gettext(u'Invalid username. Only alphabets and digits allowed.'),
        }
        return response_object, 400


    # Check email existence
    user = User.query.filter_by(email=data['email']).first()
    if user:
        response_object = {
            'status': 'fail',
            'message': gettext(u'User already exists. Please Log in.'),
        }
        return response_object, 409

    # Check duplicated username
    user = User.query.filter_by(username=data['username']).first()
    if user:
        response_object = {
            'status': 'fail',
            'message': gettext(u'Username already exists. Please choose another username.'),
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
        username=data['username'],
        password=data['password'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(new_user)
    return generate_token(new_user)


def update_user(data):
    
    try:
        user = User.query.filter_by(id=data['user_id']).first()

        if not user:
            response_object = {
                'status': 'fail',
                'message': gettext(u'User not found.'),
            }
            return response_object, 404

        # User wants to update email
        if 'email' in data.keys():

            #  Check Email format
            if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data['email']):
                response_object = {
                    'status': 'fail',
                    'message': gettext(u'Invalid email address.'),
                }

            # Check email existence
            user = User.query.filter_by(email=data['email']).first()
            if user:
                response_object = {
                    'status': 'fail',
                    'message': gettext(u'Email already exists. Please choose another.'),
                }
                return response_object, 409

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


def get_all_users():
    return User.query.all()


def get_user(id):
    return User.query.filter_by(id=id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': gettext(u'Successfully registered.'),
            'public_id': user.public_id,
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': gettext(u'Some error occurred. Please try again.')
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()

