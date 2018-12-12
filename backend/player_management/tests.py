# Create your tests here.

from django.core.wsgi import get_wsgi_application
from django.test import TestCase
from django_seed import Seed
from faker import Faker, Factory, Generator
from faker.providers import person, date_time
from player_management.models import Person, Club, PersonToClubMembership
from django.test import TestCase
from django_seed import Seed
import csv

# Define Seeding function to quickly populate database for tests

def seed_app(minimalEntityNumber : int=10):
    """
    this seeds the database with entries. Due to dependency other tables it might be
    necessary to have more entries in some tables than in ohters. In any case the
    Number of entries in each table is allways higher or equal to minimalEntityNumber

    Attributes
    ----------
    minimalEntityNumber : int
    minimal ammount of entries in each table
    """

    # TODO: implement this if the model cannot be seeded via the standard cli method./manage.py seed
    pass


def seed_person():
    fake = Factory.create(locale='de_DE')
    fake.add_provider(person)
    fake.add_provider(date_time)
    p = person.Provider(generator=Generator())

    fakePerson = Person()
    fakePerson.firstname = fake.first_name()
    fakePerson.lastname = fake.last_name()
    fakePerson.firstname = fake.first_name()


def loadcsvData():
    # TODO: Initialize data from the csv files. us the constructors for that
    pass

class testDataModel(TestCase):
    def setUp(self):

        seeder = Seed.seeder()

        seeder.add_entity(Person, 1)
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
