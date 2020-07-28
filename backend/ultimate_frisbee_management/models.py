from datetime import date

from django.db import models

from picklefield.fields import PickledObjectField, dbsafe_encode
from django.contrib.auth.models import User
from django.contrib.auth import models as authModels
from django.core.validators import MinValueValidator
from django.db.models import F, Q
from django.utils.safestring import mark_safe

from viewflow.models import Process
from imagekit.models import ProcessedImageField, ImageSpecField
from .utils.image_processing import DetectFaceAndResizeToFit
from imagekit.processors import ResizeToFit


class Eligibility(models.QuerySet):
    pass


class PersonEligibility(Eligibility):
    def u17(self):
        return self.filter(birthdate__year__gte=date.today().year - 17)

    def u20(self):
        return self.filter(birthdate__year__gte=date.today().year - 20)

    def u24(self):
        return self.filter(birthdate__year__gte=date.today().year - 24)

    def masters(self):
        return self.filter(
            (Q(birthdate__year__lte=date.today().year - 33) & Q(sex="m"))
            | (Q(birthdate__year__lte=date.today().year - 30) & Q(sex="f"))
        )


class Person(models.Model):
    """ A Person reflects one single real Person, there shall be no two person
    objects for the same Person Persons CAN be linked to users of the application,
     meaning that the person is a User of this application
    """

    SEX = [
        ["m"] * 2,
        ["f"] * 2,
    ]
    objects = PersonEligibility.as_manager()

    # personal information
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    sex = models.CharField(max_length=1, choices=SEX)
    birthdate = models.DateField()  # TODO: validator to check that date is not in the future

    # specify image directory
    # Memberships
    club_memberships = models.ManyToManyField("Club", through="PersonToClubMembership")
    team_memberships = models.ManyToManyField("Team", through="PersonToTeamMembership")
    association_memberships = models.ManyToManyField("Association", through="PersonToAssociationMembership")

    # other relationships
    roster_relationships = models.ManyToManyField("Roster", through="PersonToRosterRelationship")
    # todo this should be models.oneTooneField but the faking factory is not capable atm to build unique relationships between person and user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = ProcessedImageField(
        upload_to="images/persons/",
        processors=[ResizeToFit(width=500, height=500)],
        format="JPEG",
        options={"quality": 80},
        blank=True,
        null=True,
    )

    face = ImageSpecField(
        source="image",
        processors=[DetectFaceAndResizeToFit(width=70, height=70)],
        format="JPEG",
        options={"quality": 80},
    )

    def image_45p_tag(self):
        if self.face and hasattr(self.face, "url"):
            return mark_safe('<img src="%s" style="height:70px;" />' % self.face.url)
        else:
            return "-"

    image_45p_tag.short_description = "image"

    def image_500p_tag(self):
        if self.image and hasattr(self.image, "url"):
            return mark_safe('<img src="%s" style="max-width: 500px;" />' % self.image.url)
        else:
            return "-"

    image_500p_tag.short_description = "image"

    # elegibility
    def eligibile_u17(self) -> bool:
        return date.today().year - self.birthdate.year <= 17

    eligibile_u17.boolean = True
    eligibile_u17.short_description = "u17"

    def eligibile_u20(self) -> bool:
        return date.today().year - self.birthdate.year <= 20

    eligibile_u20.boolean = True
    eligibile_u20.short_description = "u20"

    def eligibile_u24(self) -> bool:
        return date.today().year - self.birthdate.year <= 24

    eligibile_u24.boolean = True
    eligibile_u24.short_description = "u24"

    @property
    def eligibile_masters(self):
        return self.birthdate

    @property
    def eligibile_grandmasters(self):
        return self.birthdate

    @property
    def eligibile_open(self):
        return self.birthdate

    @property
    def eligibile_women(self):
        return self.birthdate

    @property
    def eligibile_mixed(self):
        return self.birthdate

    def get_current_clubmemberships(self) -> models.QuerySet:
        today = date.today()
        this_year = date(year=today.year, month=1, day=1)
        club_memberships = PersonToClubMembership.objects.filter(person=self).filter(
            Q(valid_until__gte=this_year) | Q(valid_until__isnull=True)
        )
        return club_memberships

    def eligibile_onlyOneClub(self) -> bool:
        return self.get_current_clubmemberships().count() < 2

    eligibile_onlyOneClub.boolean = True
    eligibile_onlyOneClub.short_description = "Nur ein Verein"

    # TODO: refactor into elegibilty framework
    def eligibile_nationals(self, tournament: str, year=date.today().year) -> bool:

        current_clubs = Club.objects.filter(persontoclubmembership__in=self.get_current_clubmemberships().all())
        roster = Roster.objects.filter(
            Q(person=self)
            & Q(tournament_division__tournament__name__contains=tournament)
            & Q(tournament_division__tournament__start__year__gte=year)
            & ~Q(team__club_membership__in=current_clubs)
        )
        return roster.count() < 2

    def eligibile_nationals_ow(self):
        return self.eligibile_nationals("ÖSTM OPEN")

    eligibile_nationals_ow.boolean = True
    eligibile_nationals_ow.short_description = "El. ÖSTM OW"

    def eligibile_nationals_mixed(self):
        return self.eligibile_nationals("ÖSTM MIXED")

    eligibile_nationals_mixed.boolean = True
    eligibile_nationals_mixed.short_description = "El. ÖSTM X"

    def eligibile_nationals_beach(self):
        return self.eligibile_nationals("BÖSTM")

    eligibile_nationals_beach.boolean = True
    eligibile_nationals_beach.short_description = "El. BÖSTM"

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.birthdate.year})"

    class Meta:
        db_table = "pm_Person"


class Organisation(models.Model):
    """ An organization is an abstract concept for people or parties
    who organize themselves for a specific purpose.  Teams, clubs
    and associations are the 3 different organization types in this model"""

    name = models.CharField(max_length=300)
    founded_on = models.DateField()
    dissolved_on = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    logo = ProcessedImageField(
        upload_to="images/logos/",
        processors=[ResizeToFit(width=500, height=500)],
        format="JPEG",
        options={"quality": 80},
        blank=True,
        null=True,
    )

    def image_45p_tag(self):
        if self.logo and hasattr(self.logo, "url"):
            return mark_safe('<img src="%s" style="height:45px;" />' % self.logo.url)
        else:
            return "-"

    image_45p_tag.short_description = "logo"

    def image_500p_tag(self):
        if self.logo and hasattr(self.logo, "url"):
            return mark_safe('<img src="%s" style="max-width: 500px;" />' % self.logo.url)
        else:
            return "-"

    image_500p_tag.short_description = "logo"

    @property
    def is_active(self):
        if self.dissolved_on is None:
            return True
        elif self.dissolved_on > date.today():
            return True
        else:
            return False

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Association(Organisation):
    """ An Association (german: Verband) is a legal form of an organisation. It may represent
    people or other Organisations. In the Ultimate Frisbee context an Association represents
    multiple Clubs. By Definition it is represented by a board committee. The board is reflected
    in the PersonToAssociationMembership which defines membership roles"""

    board_members = models.ManyToManyField("Person", through="PersonToAssociationMembership")
    member_clubs = models.ManyToManyField("Club", through="ClubToAssociationMembership")
    governing_associations = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="AssociationToAssociationMembership",
        through_fields=("governor", "member"),
        related_name="association_members",
    )

    class Meta(Organisation.Meta):
        db_table = "pm_Association"


class Club(Organisation):
    member_persons = models.ManyToManyField("Person", through="PersonToClubMembership")
    associations_memberships = models.ManyToManyField("Association", through="ClubToAssociationMembership")

    class Meta(Organisation.Meta):
        db_table = "pm_Club"


class Team(Organisation):
    """ A Team is an organization owned by a Club. it consists of a list
    of players which is a temporary assignment of a player to a team"""

    club_membership = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    member_persons = models.ManyToManyField("Person", through="PersonToTeamMembership")
    tournament_divisions = models.ManyToManyField("TournamentDivision", through="Roster")

    class Meta(Organisation.Meta):
        db_table = "pm_Team"


class Event(models.Model):
    name = models.CharField(max_length=300)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class EventSeries(models.Model):
    name = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=True)
    events = models.ManyToManyField("Event")
    subseries = models.ManyToManyField("self", symmetrical=False, related_name="parent_series",)

    class Meta:
        abstract = True


class Tournament(Event):
    divisions = models.ManyToManyField("Division", through="TournamentDivision")

    def __str__(self):
        return f"{self.name} | {self.start.date()}"


class Roster(models.Model):
    """ A roster is a set of persons that compete in a Team at a TournamentDivision
        with a teamrole and number.
    """

    tournament_division = models.ForeignKey("TournamentDivision", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    persons = models.ManyToManyField("Person", through="PersonToRosterRelationship")

    # TODO: check if roster is valid

    def __str__(self):
        return f"{self.team.name} @ {self.tournament_division.__str__()}"


class TournamentDivision(models.Model):
    """ A TournamentDivision represents the hosting of a Division at a Tournament
        and contains a list of the attending teams.
    """

    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)
    division = models.ForeignKey("Division", on_delete=models.CASCADE)
    teams = models.ManyToManyField("Team", through="Roster")

    def __str__(self):
        return f"{self.tournament.name} | {self.division.name}"


class Division(models.Model):
    """ a Division is a set of rules (Queryset) that defines the
    eligibility of Persons, Teams and specific Rosters to compete at a related tournament.
    A tournament can have more than one Divsion. 

    Example: TournamentDivision Mixed EUCF. Eligible are all players who have
    not played at any EUCR in another Division and all Teams that have qualified through
    eucr and whose roster for this tournament does not contain more than 3 new players compared 
    to the EUCR roster
    """

    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)

    def default_eligible_person_query():
        return dbsafe_encode(Person.objects.all().query)

    eligible_person_query = PickledObjectField(default=default_eligible_person_query)

    def default_eligible_team_query():
        return dbsafe_encode(Team.objects.all().query)

    eligible_team_query = PickledObjectField(default=default_eligible_team_query)

    tournaments = models.ManyToManyField("Tournament", through="TournamentDivision")

    def eligible_persons(self) -> models.QuerySet:
        queryset = Person.objects.all()
        queryset.query = self.eligible_person_query
        return queryset

    # would be nice to have the AND clauses that caused the object to not be selected.
    def is_eligible(self, person: Person) -> bool:
        queryset = Person.objects.all()
        queryset.query = self.eligible_person_query

    def eligible_teams(self) -> models.QuerySet:
        queryset = Team.objects.all()
        queryset.query = self.eligible_team_query
        return queryset

    # TODO: if not elegible return lookups that caused it
    # self.query.where.children reutrns an iterable over all lookups

    def is_eligible(self, team: Team) -> bool:
        return self.eligible_Teams.filter(pk=team.pk).exists()

    def eligible_Rosters(self) -> models.QuerySet:
        queryset = Roster.objects.all()
        queryset.query = self.eligible_team_query
        return queryset

    def is_eligible(self, roster: Roster) -> bool:
        return self.eligible_Rosters.filter(pk=roster.pk).exists()

    def __str__(self):
        return f"{self.name} (id= {self.id})"


class BaseRelationship(models.Model):
    reporter: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="reported_%(class)ss",
        related_query_name="%(class)s_reporter",
        null=True,
    )
    approved_by: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="approved_%(class)ss",
        related_query_name="%(class)s_approver",
        null=True,
    )

    class Meta:
        abstract = True


class Membership(BaseRelationship):
    """ A membership connects an organization as target with another organization
    or person as member. It is reported by, and  confirmed by a person
    it my have a from and until date. missing values assume an infinite Membership period"""

    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
        # TODO: constraint does not work
        constraints = [
            models.CheckConstraint(
                check=Q(valid_from__lte=F("valid_until")),
                name="%(app_label)s_%(class)s valid_from is earlier than valid_until",
            )
        ]

    def is_active(self) -> bool:
        return self.valid_from <= date.now() <= self.valid_until


class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES = (
        ["President"] * 2,
        ["Treasurer"] * 2,
        ["Boardmember"] * 2,
    )  # there are no member roles since members are clubs

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES)

    class Meta(Membership.Meta):
        db_table = "pm_PersonToAssociationMembership"
        # TODO: constraint memberships time periods may not overlap for a person and association


class PersonToClubMembership(Membership):
    ASSOCIATION_ROLES = (
        ["President"] * 2,
        ["Treasurer"] * 2,
        ["Boardmember"] * 2,
        ["Member"] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES, default="Member")

    class Meta(Membership.Meta):
        db_table = "pm_PersonToClubMembership"
        # TODO: constraint memberships time periods may not overlap for a person and club


class PersonToTeamMembership(Membership):
    TEAM_ROLES = (
        ["Player"] * 2,
        ["Coach"] * 2,
        ["Captain"] * 2,
        ["Spiritcaptain"] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=TEAM_ROLES, default="Player", null=True)
    number = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    # TODO: remove this relationship

    class Meta(Membership.Meta):
        db_table = "pm_PersonToTeamMembership"


class ClubToAssociationMembership(Membership):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = "pm_ClubToAssociationMembership"
        # TODO: constraint memberships time periods may not overlap for a club and association


class AssociationToAssociationMembership(Membership):
    member = models.ForeignKey(Association, on_delete=models.CASCADE, related_name="association_memberships")
    governor = models.ForeignKey(Association, on_delete=models.CASCADE, related_name="association_governing")

    class Meta(Membership.Meta):
        db_table = "pm_AssociationToAssociationMembership"


class PersonToClubMembershipProcess(Process):
    membership = models.ForeignKey(PersonToClubMembership, blank=True, null=True, on_delete=models.CASCADE)
    # TODO: remove this


class PersonToRosterRelationship(BaseRelationship):
    TEAM_ROLES = (
        ["Player"] * 2,
        ["Coach"] * 2,
        ["Captain"] * 2,
        ["Spiritcaptain"] * 2,
    )

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=TEAM_ROLES, default="Player", null=True)
    number = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    # TODO: check if roster membership is valid

    class Meta(BaseRelationship.Meta):
        db_table = "pm_PersonToRosterRelationship"
        constraints = [
            models.UniqueConstraint(
                fields=["roster", "number"], condition=~Q(number=0), name="No duplicate numbers on Roster Constraint"
            ),
            models.UniqueConstraint(
                fields=["roster", "person"], name="No duplicate Person entries in Roster Constraint"
            ),
        ]

