import unittest
import json

from random import randint
from django.test import Client

from .models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        random = randint(0, 99)
        
        self.data = {
            'username': 'testCase{0}'.format(random),
            'email': 'testCase{0}@server.local'.format(random),
            'password': 'testCase{0}'.format(random),
        }
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        #http client
        self.client = Client()


    def test_register(self):
        """Test POST /api/users/ creation"""

        response = self.client.post('/api/users/', 
                data=self.data, 
                headers=self.headers
        )

        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        """Test POST /login"""

        response = self.client.post('/login', 
                data={
                    'username': self.data['username'],
                    'password': self.data['password'],
                }, 
                headers=self.headers
        )
        
        self.assertIn(response.content.decode('utf-8'), 'href="/accounts/profile"')

