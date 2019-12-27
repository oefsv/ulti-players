import pytest
# Create your tests here.
from django.contrib.auth.models import User
from ..models import Person, Club, PersonToClubMembership
from django.test import TestCase
from django_seed import Seed
from mixer.backend.django import mixer
import pytest
from django.contrib.auth.models import User
from rest_auth.views import UserDetailsView
from rest_auth.serializers import UserDetailsSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.reverse import reverse_lazy
from rest_framework import status
from mixer.backend.django import mixer

class TestViews(APITestCase):
    def setUp(self):
        self.factory: APIRequestFactory = APIRequestFactory()

    def test_get_user_profile(self):

        view = UserDetailsView()
        user = mixer.blend(User)

        path = reverse_lazy('rest_auth:rest_user_details')
        request = self.factory.get(path)
        request.user = user
        response = view.dispatch(request)

        serializer = UserDetailsSerializer(user)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == serializer.data['pk']



@pytest.mark.django_db
class TestModel(TestCase):

    def setUp(self):

       self.club = mixer.blend(Club)
       self.person = mixer.blend(Person)

    def test_PersonToClubMembership(self):
        """create a person and a club add person to club test isActive function"""

        PersonToClubMembership.objects.create(person=self.person,club=self.club,role="Treasurer",valid_from="2019-09-09")

        role = PersonToClubMembership.objects.get(person=self.person, club=self.club).role

        self.assertTrue(role == 'Treasurer')

    def test_getCurrentUserClubs(self):
        assert True

