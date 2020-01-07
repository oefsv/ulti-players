import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestAdmin(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='12345')
    
    def test_url(self):
        path = reverse('admin:ultimate_frisbee_management_person_changelist')
        response = self.client.get(path)
        assert response