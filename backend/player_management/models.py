from datetime import date
from random import choices
from rlcompleter import get_class_members

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as authModels
from django.core.validators import MinValueValidator
from viewflow.models import Process


class Person(models.Model):
    """ A Person reflects one single real Person, there shall be no two person
    objects for the same Person Persons CAN be linked to users of the application,
     meaning that the person is a User of this application
    """
    SEX = [
        ['m'] * 2,
        ['f'] * 2,
    ]

    # personal information
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    sex = models.CharField(max_length=1, choices=SEX)
    birthdate = models.DateField() # TODO: validator to check that date is not in the future

    # Memberships
    club_memberships = models.ManyToManyField('Club', through='PersonToClubMembership')
    team_memberships = models.ManyToManyField('Team', through='PersonToTeamMembership')
    association_memberships = models.ManyToManyField('Association', through='PersonToAssociationMembership')
    ## todo this should me models.oneTooneField but the faking factory is not capable atm to build unique relationships between person and user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pm_Person'


class Organisation(models.Model):
    """ An organization is an abstract concept for people or parties
    who organize themselves for a specific purpose.  Teams, clubs
    and associations are the 3 different organization types in this model"""
    name = models.CharField(max_length=300)
    founded_on = models.DateField()
    dissolved_on = models.DateField(null=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class Association(Organisation):
    """ An Association (german: Verband) is a legal form of an organisation. It may represents
    people or other Organisations. In the Ultimate Frisbee context an Association represents
    multiple Clubs. By Definition it is represented by a board committee. The board is reflected
    in the PersonToAssociationMembership which defines membership roles"""
    # TODO:
    board_members = models.ManyToManyField('Person', through='PersonToAssociationMembership')
    member_clubs = models.ManyToManyField('Club', through='ClubToAssociationMembership')
    governing_associations = models.ManyToManyField(
        'self',
        symmetrical= False,
        through='AssociationToAssociationMembership',
        through_fields=('governor','member'),
        related_name='association_members',
    )

    class Meta(Organisation.Meta):
        db_table = 'pm_Association'


class Club(Organisation):
    member_persons = models.ManyToManyField('Person', through='PersonToClubMembership')
    associations_memberships = models.ManyToManyField('Club',through='ClubToAssociationMembership')

    class Meta(Organisation.Meta):
        db_table = 'pm_Club'


class Team(Organisation):
    """ A Team is an organization owned by a Club. it consists of a list
    of players which is antemporary assignment of a player to a team"""
    club_membership = models.ForeignKey(Club, on_delete=models.CASCADE)
    member_persons = models.ManyToManyField('Person', through='PersonToTeamMembership')

    class Meta(Organisation.Meta):
        db_table = 'pm_Team'


class Membership(models.Model):
    """ A membership connects an organization as target with another organozation
    or person as member. It is reported by, and  confirmed by a person
    it my have a from and until date. missing values asumen an infinite Membership period"""

    valid_from = models.DateField()
    valid_until = models.DateField()

    reporter: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="reported_%(class)ss",
        related_query_name="%(class)s_reporter")
    approved_by: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="approved_%(class)ss",
        related_query_name="%(class)s_approver")

    class Meta:
        abstract = True

    def is_active(self) -> bool:
        return self.valid_from <= date.now() <= self.valid_until


class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES = (
        ['President'] * 2,
        ['Vicepresident'] * 2,
        ['Treasurer'] * 2,
        ['secretary'] * 2,
    ) # there are no member roles since members are clubs

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES)

    class Meta(Membership.Meta):
        db_table = 'pm_PersonToAssociationMembership'


class PersonToClubMembership(Membership):
    ASSOCIATION_ROLES = (
        ['President'] * 2,
        ['Vicepresident'] * 2,
        ['Treasurer'] * 2,
        ['secretary'] * 2,
        ['Member'] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES,default='Member')

    class Meta(Membership.Meta):
        db_table = 'pm_PersonToClubMembership'


class PersonToTeamMembership(Membership):
    TEAM_ROLES = (
        ['Player'] * 2,
        ['Coach'] * 2,
        ['Captain'] * 2,
        ['Spiritcaptain'] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=TEAM_ROLES, default='')
    number = models.IntegerField(validators=[MinValueValidator(0)]) # should maxValue==42 ?

    class Meta(Membership.Meta):
        db_table = 'pm_PersonToTeamMembership'


class ClubToAssociationMembership(Membership):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'pm_ClubToAssociationMembership'


class AssociationToAssociationMembership(Membership):
    member = models.ForeignKey(Association, on_delete=models.CASCADE,related_name='association_memberships')
    governor = models.ForeignKey(Association, on_delete=models.CASCADE,related_name='association_governing')

    class Meta(Membership.Meta):
        db_table = 'pm_AssociationToAssociationMembership'