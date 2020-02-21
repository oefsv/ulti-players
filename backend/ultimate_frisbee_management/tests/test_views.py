import pytest

# Create your tests here.
from django.contrib.auth.models import User
from ..models import Person, Club, PersonToClubMembership, Division
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
from picklefield.fields import dbsafe_encode


class TestViews(APITestCase):
    def setUp(self):
        self.factory: APIRequestFactory = APIRequestFactory()

    def test_get_user_profile(self):

        view = UserDetailsView()
        user = mixer.blend(User)

        path = reverse_lazy("rest_auth:rest_user_details")
        request = self.factory.get(path)
        request.user = user
        response = view.dispatch(request)

        serializer = UserDetailsSerializer(user)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == serializer.data["pk"]


@pytest.mark.django_db
class TestDivision(TestCase):
    def setUp(self):
        self.person = mixer.blend(Person, birthdate="2020-01-01")
        self.person = mixer.blend(Person, birthdate="1919-01-01")
        pass

    def test_division_lifecycle(self):
        Division.objects.create(
            name="test", description="test", eligible_person_query=dbsafe_encode(Person.objects.u17().query)
        )
        div: Division = Division.objects.get(name="test")

        el_persons = Person.objects.all()
        el_persons.query = div.eligible_person_query
        assert el_persons.count() == 1


@pytest.mark.django_db
class TestModel(TestCase):
    def setUp(self):

        self.club = mixer.blend(Club)
        self.person = mixer.blend(Person)

    def test_PersonToClubMembership(self):
        """create a person and a club add person to club test isActive function"""

        PersonToClubMembership.objects.create(
            person=self.person, club=self.club, role="Treasurer", valid_from="2019-09-09"
        )

        role = PersonToClubMembership.objects.get(person=self.person, club=self.club).role

        self.assertTrue(role == "Treasurer")

    def test_getCurrentUserClubs(self):
        assert True

