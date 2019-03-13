import unittest

from app.main import db
from app.main.user_auth.models.blacklist_token import BlacklistToken
import json
from app.test.base import BaseTestCase

correct_admin_login_details = dict (
    username='testadmin',
    password= 'test123456'
)


def login_admin(self, admin_login_details):
    return self.client.post(
        '/api/auth/admin/login',
        data=json.dumps(admin_login_details),
        content_type='application/json'
    )

class TestAuthBlueprint(BaseTestCase):
    def test_login(self):
        """ Test for admin login with correct username and password """
        with self.client:
            response = login_admin(self, correct_admin_login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'])
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')


    def test_login_incorrect(self):
        """ Test for admin login with incorrect username or password """
        with self.client:

            # Incorrect username
            admin_login_details = correct_admin_login_details.copy()
            admin_login_details['username'] = 'wrong_un' + admin_login_details['username'];
            response = login_admin(self, admin_login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'])
            self.assertTrue(data['error_code'] == 4031)
            self.assertTrue(response.content_type == 'application/json')

            # Incorrect password
            admin_login_details = correct_admin_login_details.copy()
            admin_login_details['password'] = 'wrong_pass' + admin_login_details['password'];
            response = login_admin(self, admin_login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'])
            self.assertTrue(data['error_code'] == 4031)
            self.assertTrue(response.content_type == 'application/json')

            # Incorrect username and password
            admin_login_details = correct_admin_login_details.copy()
            admin_login_details['username'] = 'wrong_un' + admin_login_details['username'];
            admin_login_details['password'] = 'wrong_pass' + admin_login_details['password'];
            response = login_admin(self, admin_login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'])
            self.assertTrue(data['error_code'] == 4031)
            self.assertTrue(response.content_type == 'application/json')
            

    def test_logout(self):
        """ Test for admin logout """
        with self.client:

            # Login
            response = login_admin(self, correct_admin_login_details)
            
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'])
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')

            token = data['token']

            # valid token logout
            response = self.client.post(
                '/api/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

            # logout with a blacklisted token
            response = self.client.post(
                '/api/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['error_code'] == 4032)

            # logout with an invalid token
            response = self.client.post(
                '/api/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + token + 'this_make_token_invalid'
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['error_code'] == 4034)