import pytest
# Create your tests here.

from django.core.wsgi import get_wsgi_application
from django.test import TestCase
from django_seed import Seed
from faker import Faker, Factory, Generator
from faker.providers import person, date_time
from ..models import Person, Club, PersonToClubMembership
from django.test import TestCase
from django_seed import Seed
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestModel:

    def test_ceate_user(self):
        user = mixer.blend('auth.user', username='test')
        assert user.username == "test"


class testDataModel(TestCase):

    def setUp(self):

        seeder = Seed.seeder()


        #seeder.add_entity(Person, 1)
        seeder.add_entity(Club, 1)

        inserted_pks = seeder.execute()

        person_id = inserted_pks[Person][0]
        club_id = inserted_pks[Club][0]

        PersonToClubMembership(person_id=person_id, club_id=club_id)


    def test_PersonToClubMembership(self):
        """create a person and a club add person to club test isActive function"""

        person = Person.objects.all()[0]
        club = person.club_memberships.all()[0]
        role = PersonToClubMembership.objects.get(person=person, club=club).role

        self.assertTrue(role == 'Member')

    def test_getCurrentUserClubs(self):
        pass

    def test_create_Person_without_User(self):
        assert false

    def test_create_Person_with_creating_User(self):
        assert false

    def test_create_Person_with_existing_User(self):
        assert false
