from django.test import TestCase

from rest_framework.test import APIClient

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
