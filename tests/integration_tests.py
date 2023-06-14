from flask_testing import TestCase
from app import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_register(self):
        response = self.client.post('/register', json={
            "firstname": "ale",
            "lastname": "bledea",
            "gender": "female",
            "email": "ale31@yahoo.com",
            "password": "a"
        })
        self.assert200(response)
        self.assertEqual(response.json, {'Message': 'Account created successfully!'})

    def test_register_invalid_emal(self):
        response = self.client.post('/register', json={
            "firstname": "ale",
            "lastname": "bledea",
            "gender": "female",
            "email": "ale21@yahoo.com",
            "password": "a"
        })
        self.assert200(response)
        self.assertEqual(response.json, {'Message': 'There exists an account with the given email!'})

    def test_change_password(self):
        response = self.client.put('/login/change-password', json={
            "email": "ale21@yahoo.com",
            "oldPassword": "b",
            "newPassword": "a"
        })
        self.assert200(response)
        self.assertEqual(response.json, {'Message': 'Password changed successfully!'})

    def test_change_password_invalid_email(self):
        response = self.client.put('/login/change-password', json={
            "email": "ale21221@yahoo.com",
            "oldPassword": "a",
            "newPassword": "b"
        })
        self.assert200(response)
        self.assertEqual(response.json, {'Message': 'Invalid password or email'})


    def test_change_password_invalid_password(self):
        response = self.client.put('/login/change-password', json={
            "email": "ale21@yahoo.com",
            "oldPassword": "abba",
            "newPassword": "b"
        })
        self.assert200(response)
        self.assertEqual(response.json, {'Message': 'Invalid password or email'})