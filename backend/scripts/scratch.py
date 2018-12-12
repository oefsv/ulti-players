from django.core.wsgi import get_wsgi_application
from faker import Faker, Factory, Generator
from faker.providers import person, date_time

from player_management.models import Person
application = get_wsgi_application()



def seed_person():
    fake = Factory.create(locale='de_DE')
    fake.add_provider(person)
    fake.add_provider(date_time)
    p = person.Provider(generator=Generator())

    fakePerson = Person()
    fakePerson.firstname = fake.first_name()
    fakePerson.lastname = fake.last_name()
    fakePerson.firstname = fake.
    fakePerson.firstname = fake.first_name()


def fakeDBdata(N):
    """ Insert N random generated  objects for each Model in this app"""

    for i in range(0,N):
        seed_person()

if __name__ == "__main__":
    fakeDBdata(1)

