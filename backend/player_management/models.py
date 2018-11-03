from datetime import date
from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as authModels


class Person(models.Model):
    """
    A Person reflects one single real Person, there shall be no two person
    objects for the same Person Persons CAN be linked to users of the application,
     meaning that the person is a User of this application
    """
    SEX = [
        ['male'] * 2,
        ['female'] * 2,
    ]
    """ personal information"""
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthdate = models.DateField()
    sex = models.CharField(max_length=5, choices=SEX)

    """  contact information"""
    email = models.EmailField()
    zip = models.PositiveIntegerField(blank=True)


class Organisation(models.Model):
    """ An organization is an abstract concept for people or parties
    who organize themselves for a specific purpose.  Teams, clubs
    and associations are the 3 different organization types in this model"""
    name = models.CharField(max_length=300)
    founded_on = models.DateField()
    dissolved_on = models.DateField()
    description = models.TextField()

    class Meta:
        abstract = True


class Association(Organisation):
    """ An Association (german: Verband) is an Organisation that represents individuals or
    other organisations for a common Goal. In the Ultimate Frisbee context an Association
    represents multiple Clubs."""

    class Meta(Organisation.Meta):
        db_table = 'Association'


class Club(Organisation):
    class Meta(Organisation.Meta):
        db_table = 'Club'


class Team(Organisation):
    """ A Team is an organization owned by a Club. it consists of a list
    of players which is antemporary assignment of a player to a team"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta(Organisation.Meta):
        db_table = 'Team'


class Player(models.Model):
    """A player is a role of aperson in context of the sport.
    it holds"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()


class Membership(models.Model):
    """ A membership connects an organization with another organozation
    or peraon. It is reported by, and  confirmed by a person
    it my have a from and until date. missing values asumen an infinite Membership period"""

    valid_until = models.DateField()
    valid_from = models.DateField()
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


class PersonToTeamMembership(Membership):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="TeamMemberships")
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    class Meta(Membership.Meta):
        db_table = 'PlayerToTeamMembership'


class ClubToAssociationMembership(Membership):
    team = models.ForeignKey(Club, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'ClubToAssociationMembership'


class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES = (
        ['President'] * 2,
        ['Vicepresident'] * 2,
        ['Treasurer'] * 2,
        ['secretary'] * 2,
        ['Member'] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES)

    class Meta(Membership.Meta):
        db_table = 'PersonToAssociationMembership'
