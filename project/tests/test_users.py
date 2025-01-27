import json
from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


class TestUserService(BaseTestCase):
    @staticmethod
    def add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def test_users(self):
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
            '/users',
            data=json.dumps(
                dict(username='michael',
                     email="michael@realpython.com")
            ),
            content_type='application/json',
        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@realpython.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """
        Ensure error is thrown if the JSON object is empty
        """
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict()),
                content_type='applicaiton/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object doesn't have a username key"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='michael@realpython.com')),
                content_type='applicaiton/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        self.client.post(
            '/users',
            data=json.dumps(dict(
                username='michael',
                email='michael@realpython.com'
            )),
            content_type='application/json',
        )

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='michael',
                    email='michael@realpython.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            print(data)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves """
        user = self.add_user('michael', 'michael@realpython.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response= self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@realpython.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        self.add_user('michael', 'michael@realpython.com')
        self.add_user('fletcher', 'fletcher@realpython.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn(
                'michael@realpython.com', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn(
                'fletcher@realpython.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
    added to the database."""
        self.add_user('michael', 'michael@realpython.com')
        self.add_user('fletcher', 'fletcher@realpython.com')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertNotIn(b'<p>No users!</p>', response.data)
        self.assertIn(b'<strong>michael</strong>', response.data)
        self.assertIn(b'<strong>fletcher</strong>', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='michael', email='michael@realpython.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'<strong>michael</strong>', response.data)












