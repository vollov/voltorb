from django.test import TestCase

from rest_framework.test import APIClient
from django.contrib.auth import authenticate

###############################################
## test user registration 
###############################################
class TestUserAuthentication(TestCase):
    # fixtures = ['accounts.json',]
    
    def test_registration(self):
        
        client = APIClient()
        
        user = {'username': 'martin',
             'first_name': 'Martin',
             'last_name': 'Bright',
             'email':'martin@abc.com',
             'password':'pwd123',
             'confirm_password':'pwd123'}
        response = client.post('/api/register', user, format='json')
        # print response
        assert response.status_code == 201

    def test_authenticate_with_username(self):
        """
        all-winterpass
        """
        user = authenticate(username='kate', password='winterpass')
        self.assertIsNotNone(user, msg='authenticate with username should return user')
        
        if user is not None:
            print 'authenticate with user success'
        else:
            print 'No backend authenticated the credentials'

    def test_login(self):
        client = APIClient()
        user = {'username':'dustin ',
                'password': 'winterpass'}
         
        response = client.post('/api/login/', user, format='json')
        # print response.data
        assert response.status_code == 200