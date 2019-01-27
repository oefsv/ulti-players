from django.contrib.auth.models import User
from django.test import TestCase, client

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .views import startSession


class testApiStartSession(TestCase):

    def setUp(self):
        User.objects.create_user(username="test",
                                 email='test@test.com',
                            password="test")

    def test_Session_Start(self):
        factory = APIRequestFactory()
        c = client.Client()
        response=c.post('/rest-auth/session/login',
                               {'username': 'test',
                                'password': 'test'}
                               )
        test= (hasattr(response,'cookies') and
            'sessionid' in response.cookies and
            'user' in response.cookies)
        self.assertTrue(test)
