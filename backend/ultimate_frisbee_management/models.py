from datetime import date
from random import choices
from rlcompleter import get_class_members

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as authModels
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.utils.safestring import mark_safe

from viewflow.models import Process
from imagekit.models import ProcessedImageField, ImageSpecField
from .utils.image_processing import DetectFaceAndResizeToFit
from imagekit.processors import ResizeToFit


# Custom Mixins



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
    birthdate = models.DateField()  # TODO: validator to check that date is not in the future

    # specify image directory
    # Memberships
    club_memberships = models.ManyToManyField('Club', through='PersonToClubMembership')
    team_memberships = models.ManyToManyField('Team', through='PersonToTeamMembership')
    association_memberships = models.ManyToManyField('Association', through='PersonToAssociationMembership')
    ## todo this should me models.oneTooneField but the faking factory is not capable atm to build unique relationships between person and user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = ProcessedImageField(upload_to="images/persons/",
                                           processors=[ResizeToFit(width=500,height=500)],
                                           format='JPEG',
                                           options={'quality': 80},blank=True, null=True)

    face = ImageSpecField(source='image',
                                processors=[DetectFaceAndResizeToFit(width=70,height=70)],
                                format='JPEG',
                                options={'quality': 80})




    def image_45p_tag(self):
        if self.face and hasattr(self.face,'url'):
            return mark_safe('<img src="%s" style="height:70px;" />' % self.face.url)
        else:
            return '-'
    image_45p_tag.short_description = 'image'

    def image_500p_tag(self):
        if self.image and hasattr(self.image,'url'):
            return mark_safe('<img src="%s" style="max-width: 500px;" />' % self.image.url)
        else:
            return '-'
    image_500p_tag.short_description = 'image'

    # elegibility
    @property
    def eligibile_u17(self) -> bool:
        return date.today().year - self.birthdate .year <= 17
        
    @property
    def eligibile_u20(self) -> bool:
        return date.today().year - self.birthdate.year <= 20

    @property
    def eligibile_u24(self) -> bool:
        return date.today().year - self.birthdate.year <= 24

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
        club_memberships =  PersonToClubMembership.objects.filter(person=self).filter(
            Q(valid_until__gte=this_year)|
            Q(valid_until__isnull=True))  
        return club_memberships

    @property
    def eligibile_nationals(self) -> bool:
        return self.get_current_clubmemberships().count() < 2


    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.birthdate.year})"

    class Meta:
        db_table = 'pm_Person'


class Organisation(models.Model):
    """ An organization is an abstract concept for people or parties
    who organize themselves for a specific purpose.  Teams, clubs
    and associations are the 3 different organization types in this model"""
    name = models.CharField(max_length=300)
    founded_on = models.DateField()
    dissolved_on = models.DateField(blank=True,null=True)
    description = models.TextField(blank=True)
    logo = ProcessedImageField(upload_to="images/logos/",
                                           processors=[ResizeToFit(width=500,height=500)],
                                           format='JPEG',
                                           options={'quality': 80},blank=True, null=True)

    def image_45p_tag(self):
        if self.logo and hasattr(self.logo,'url'):
            return mark_safe('<img src="%s" style="height:45px;" />' % self.logo.url)
        else:
            return '-'
    image_45p_tag.short_description = 'logo'

    def image_500p_tag(self):
        if self.logo and hasattr(self.logo,'url'):
            return mark_safe('<img src="%s" style="max-width: 500px;" />' % self.logo.url)
        else:
            return '-'
    image_500p_tag.short_description = 'logo'


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
    # TODO:
    board_members = models.ManyToManyField('Person', through='PersonToAssociationMembership')
    member_clubs = models.ManyToManyField('Club', through='ClubToAssociationMembership')
    governing_associations = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='AssociationToAssociationMembership',
        through_fields=('governor', 'member'),
        related_name='association_members',
    )

    class Meta(Organisation.Meta):
        db_table = 'pm_Association'


class Club(Organisation):
    member_persons = models.ManyToManyField('Person', through='PersonToClubMembership')
    associations_memberships = models.ManyToManyField('Association', through='ClubToAssociationMembership')

    class Meta(Organisation.Meta):
        db_table = 'pm_Club'


class Team(Organisation):
    """ A Team is an organization owned by a Club. it consists of a list
    of players which is a temporary assignment of a player to a team"""
    club_membership = models.ForeignKey(Club, on_delete=models.CASCADE, null=True,blank=True)
    member_persons = models.ManyToManyField('Person', through='PersonToTeamMembership')

    class Meta(Organisation.Meta):
        db_table = 'pm_Team'


class Membership(models.Model):
    """ A membership connects an organization as target with another organization
    or person as member. It is reported by, and  confirmed by a person
    it my have a from and until date. missing values assume an infinite Membership period"""

    valid_from = models.DateField()
    valid_until = models.DateField(null=True,blank=True)

    reporter: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="reported_%(class)ss",
        related_query_name="%(class)s_reporter",
        null=True)
    approved_by: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="approved_%(class)ss",
        related_query_name="%(class)s_approver",
        null=True)

    @property
    def is_active(self):
        if self.valid_until is None:
            return True
        elif self.dissolved_on > date.today():
            return True
        else:
            return False

    class Meta:
        abstract = True

    def is_active(self) -> bool:
        return self.valid_from <= date.now() <= self.valid_until


class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES = (
        ['President'] * 2,
        ['Vicepresident'] * 2,
        ['Treasurer'] * 2,
        ['Secretary'] * 2,
    )   # there are no member roles since members are clubs

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
        ['Secretary'] * 2,
        ['Member'] * 2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES, default='Member')

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
    role = models.CharField(max_length=300, choices=TEAM_ROLES, default='Player',null=True)
    number = models.IntegerField(validators=[MinValueValidator(0)],null=True,blank=True)     # TODO: should maxValue==42 ?

    class Meta(Membership.Meta):
        db_table = 'pm_PersonToTeamMembership'


class ClubToAssociationMembership(Membership):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'pm_ClubToAssociationMembership'


class AssociationToAssociationMembership(Membership):
    member = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='association_memberships')
    governor = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='association_governing')

    class Meta(Membership.Meta):
        db_table = 'pm_AssociationToAssociationMembership'


class PersonToClubMembershipProcess(Process):
    membership = models.ForeignKey(PersonToClubMembership, blank=True, null=True, on_delete=models.CASCADE)
