

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
