import json
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('ponxg!', data['message'])
        self.assertIn('success', data['status'])








