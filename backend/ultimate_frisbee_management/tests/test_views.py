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

        seeder = Seed.seeder()


        #seeder.add_entity(Person, 1)
        seeder.add_entity(Club, 1)

        inserted_pks = seeder.execute()

#        person_id = inserted_pks[Person][0]
        club_id = inserted_pks[Club][0]

   #     PersonToClubMembership(person_id=person_id, club_id=club_id)


    def test_PersonToClubMembership(self):
        """create a person and a club add person to club test isActive function"""

        person = Person.objects.all()[0]
        club = person.club_memberships.all()[0]
        role = PersonToClubMembership.objects.get(person=person, club=club).role

        self.assertTrue(role == 'Member')

    def test_getCurrentUserClubs(self):
        assert False

    def test_create_Person_without_User(self):
        person = mixer.blend(Person)
        user = person.user
        assert user is None

    def test_create_Person_with_creating_User(self):
        person1 = mixer.blend(Person)
        person2 = mixer.blend(Person)
        user = mixer.blend(User)
        person1.user = user
        person1.save()

        personDB = Person.objects.get(pk=person1.pk)
        assert personDB == person1

    def test_create_Person_with_existing_User(self):
        person1 = mixer.blend(Person)
        person2 = mixer.blend(Person)
        user = mixer.blend(User)
        person1.user = user
        person1.save()

        personDB = Person.objects.get(pk=person1.pk)
        assert personDB == person1

    def test_ceate_user(self):
        user = mixer.blend(User, username='test')
        user = User.objects.get(username="test")
        assert user.username == "test"

