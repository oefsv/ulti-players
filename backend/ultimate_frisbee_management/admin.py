import math

from django.contrib import admin
from django.contrib.auth.models import User
from . import models, views
from .utils import mail
from datetime import date, timedelta
from django.db.models import Count, Q
from django import forms
from django.conf import settings

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import redirect
from urllib.request import Request
from django.http.request import HttpRequest

# Register your models here..


class Base_Inline(admin.TabularInline):
    show_change_link = True
    save_as = True
    extra = 0


class BaseRelationship_Inline(Base_Inline):
    model = models.BaseRelationship
    exclude = ["reporter", "approved_by"]


class Person_To_Roster_Relationship_Inline(BaseRelationship_Inline):
    model = models.PersonToRosterRelationship
    autocomplete_fields = ("person", "roster")
    verbose_name = "Person to Roster"
    verbose_name_plural = "Persons on the Roster"
    fields = ("id", "roster", "person", "division", "role", "number")
    readonly_fields = (
        "team",
        "tournament",
        "division",
    )
    show_change_link = True

    def team(self, obj):
        return obj.roster.team.name

    def tournament(self, obj):
        return obj.roster.tournament_division.tournament.name

    def division(self, obj):
        return obj.roster.tournament_division.division.name


class Roster_To_Person_Relationship_Inline(Person_To_Roster_Relationship_Inline):
    verbose_name = "Roster"
    verbose_name_plural = "Rosters listed on"


class BaseMembership_Inline(BaseRelationship_Inline):
    ordering = ("valid_until",)


class Active_Membership_Inline(BaseMembership_Inline):
    def get_queryset(self, request):
        return super().get_queryset(request).active()


class Inactive_Membership_Inline(BaseMembership_Inline):
    def get_queryset(self, request):
        return super().get_queryset(request).inactive()


class Person_to_Team_Inline(BaseMembership_Inline):
    model = models.PersonToTeamMembership
    autocomplete_fields = ("person", "team")
    list_filter = autocomplete_fields
    # readonly_fields = ("person","team","role")
    verbose_name = "Person to Team"
    verbose_name_plural = "Persons in the Team"


class Team_to_Person_Inline(Person_to_Team_Inline):
    verbose_name = "Team Membership"
    verbose_name_plural = "Team Memberships"


class Person_to_Club_Inline(Active_Membership_Inline):
    model = models.PersonToClubMembership
    autocomplete_fields = ("person", "club")
    list_filter = autocomplete_fields
    verbose_name = "Person to Club"
    verbose_name_plural = "Persons in the Club"


class Inactive_Person_to_Club_Inline(Inactive_Membership_Inline):
    model = models.PersonToClubMembership
    autocomplete_fields = ("person", "club")
    list_filter = autocomplete_fields
    verbose_name = "former Person to Club"
    verbose_name_plural = "Former Persons in the Club"


class Club_to_Person_Inline(Person_to_Club_Inline):
    verbose_name = "Club Membership"
    verbose_name_plural = "Club Memberships"


class Inactive_Club_to_Person_Inline(Inactive_Person_to_Club_Inline):
    verbose_name = "former Club Membership"
    verbose_name_plural = "Former Club Memberships"


class Person_to_Association_Inline(Active_Membership_Inline):
    model = models.PersonToAssociationMembership
    autocomplete_fields = ("association", "person")
    verbose_name = "Person to the Association"
    verbose_name_plural = "Persons in the Association"


class Inactive_Person_to_Association_Inline(Inactive_Membership_Inline):
    model = models.PersonToAssociationMembership
    autocomplete_fields = ("association", "person")
    verbose_name = "former Person to the Association"
    verbose_name_plural = "Former Persons in the Association"


class Association_to_Person_Inline(Person_to_Association_Inline):
    verbose_name = "Association Membership"
    verbose_name_plural = "Association Memberships"


class Inactive_Association_to_Person_Inline(Inactive_Person_to_Association_Inline):
    verbose_name = "former Association Membership"
    verbose_name_plural = "Former Association Memberships"


class Club_to_Association_Inline(BaseRelationship_Inline):
    model = models.ClubToAssociationMembership
    autocomplete_fields = ("association", "club")
    verbose_name = "Club to Association"
    verbose_name_plural = "Clubs in the Association"


class Association_To_Club_Inline(Club_to_Association_Inline):
    verbose_name = "Association Membership"
    verbose_name_plural = "Association Memberships"


class Member_Association_to_Association_Inline(BaseMembership_Inline):
    model = models.AssociationToAssociationMembership
    fk_name = "governor"
    autocomplete_fields = ("member", "governor")
    list_filter = autocomplete_fields
    verbose_name = "Member Association"
    verbose_name_plural = "Member Associations"


class Association_to_Member_Association_Inline(Member_Association_to_Association_Inline):
    fk_name = "member"
    verbose_name = "Parent Association"
    verbose_name_plural = "Parent Associations"


class TournamentDivision_Inline(Base_Inline):
    model = models.TournamentDivision
    autocomplete_fields = ("division",)
    show_change_link = False


class Roster_Inline(Base_Inline):
    model = models.Roster
    autocomplete_fields = ("team", "persons", "tournament_division")


class BaseFilter(admin.SimpleListFilter):
    title = "eligibile"
    parameter_name = "eligibile"
    age = 0

    def lookups(self, request, model_admin):
        return (
            ("Yes", "Yes"),
            ("No", "No"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        startdate = date.today() + timedelta(days=-self.age * 365)
        enddate = date.today()
        if value == "Yes":
            return queryset.filter(birthdate__range=[startdate, enddate])
        elif value == "No":
            return queryset.exclude(birthdate__range=[startdate, enddate])
        return queryset


class Eligibile_u17(BaseFilter):
    title = "Eligibile_u17"
    parameter_name = "Eligibile_u17"
    age = 17


class Eligibile_u20(BaseFilter):
    title = "Eligibile_u20"
    parameter_name = "Eligibile_u20"
    age = 20


class Eligibile_u24(BaseFilter):
    title = "Eligibile_u24"
    parameter_name = "Eligibile_u24"
    age = 24


class Eligible_onlyOneClub(admin.SimpleListFilter):
    title = "nur ein Verein"
    parameter_name = "Eligible_onlyOneClub"
    age = 0

    def lookups(self, request, model_admin):
        return (
            ("Yes", "Yes"),
            ("No", "No"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        today = date.today()
        this_year = date(year=today.year, month=1, day=1)
        if value == "Yes":
            return (
                queryset.filter(
                    Q(persontoclubmembership__valid_until__gte=this_year)
                    | Q(persontoclubmembership__valid_until__isnull=True)
                )
                .annotate(clubs_count=Count("club_memberships"))
                .filter(clubs_count__lt=2)
            )
        elif value == "No":
            return (
                queryset.filter(
                    Q(persontoclubmembership__valid_until__gte=this_year)
                    | Q(persontoclubmembership__valid_until__isnull=True)
                )
                .annotate(clubs_count=Count("club_memberships"))
                .filter(clubs_count__gte=2)
            )
        return queryset


class Eligible_Nationals_BaseFilter(admin.SimpleListFilter):
    title = "Eligible ÖSTM"
    parameter_name = "eligible_nationals"
    event_name = ""

    def lookups(self, request, model_admin):
        return (
            ("Yes", "Yes"),
            ("No", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            persons = [p.pk for p in queryset if (p.eligibile_nationals(self.event_name))]
            return queryset.filter(pk__in=persons)
        elif self.value() == "No":
            persons = [
                p.pk for p in queryset if (not p.eligibile_nationals(self.event_name))
            ]
            return queryset.filter(pk__in=persons)
        return queryset


class Eligible_Nationals_O(Eligible_Nationals_BaseFilter):
    title = "Eligible ÖSTM OPEN"
    parameter_name = "eligible_nationals_o"
    event_name = "ÖSTM OPEN"


class Eligible_Nationals_W(Eligible_Nationals_BaseFilter):
    title = "Eligible ÖM DAMEN"
    parameter_name = "eligible_nationals_w"
    event_name = "ÖM WOMEN"


class Eligible_Nationals_X(Eligible_Nationals_BaseFilter):
    title = "Eligible ÖSTM Mixed"
    parameter_name = "eligible_nationals_x"
    event_name = "ÖSTM MIXED"


class Eligible_Nationals_BEACH(Eligible_Nationals_BaseFilter):
    title = "Eligible BÖSTM OPEN"
    parameter_name = "eligible_nationals_beach"
    event_name = "BÖSTM"


class CustomGuardedModelAdmin(GuardedModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return request.user.has_perm(f"change_{type(obj).__name__.lower()}", obj)
        return super().has_change_permission(request, obj=obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return request.user.has_perm(f"view_{type(obj).__name__.lower()}", obj)
        return super().has_view_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return request.user.has_perm(f"delete_{type(obj).__name__.lower()}", obj)
        return super().has_delete_permission(request, obj=obj)

    save_as = True


class customFilteredGuardedModelAdmin(CustomGuardedModelAdmin):
    def get_queryset(self, request):
        objects = get_objects_for_user(
            user=request.user,
            perms=[f"view_{self.model.__name__.lower()}"],
            klass=self.model,
            accept_global_perms=False,
        )
        return objects


class PersonForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # check if an instance is parsed if not then a new object is added
        if "instance" in kwargs and kwargs["instance"] is not None:
            self.initial["email"] = kwargs["instance"].user.email

    class Meta:
        model = models.Person
        exclude = ["user"]


class PersonAdmin(GuardedModelAdmin):
    list_display = (
        "firstname",
        "lastname",
        "image_45p_tag",
        "birthdate",
        "sex",
        "eligibile_u17",
        "eligibile_u20",
        "eligibile_u24",
        "eligibile_onlyOneClub",
        "eligibile_nationals_w",
        "eligibile_nationals_o",
        "eligibile_nationals_mixed",
        "eligibile_nationals_beach",
    )

    readonly_fields = ["image_500p_tag"]
    # editable list fields cause huge performance issues when in debug mode
    # if not settings.DEBUG:
    #    list_editable = ("lastname", "sex", "birthdate")

    list_filter = (
        Eligibile_u17,
        Eligibile_u20,
        Eligibile_u24,
        Eligible_onlyOneClub,
        Eligible_Nationals_W,
        Eligible_Nationals_O,
        Eligible_Nationals_X,
        Eligible_Nationals_BEACH,
    )
    list_display_links = ("firstname",)
    search_fields = ("firstname", "lastname", "birthdate")
    inlines = (
        Club_to_Person_Inline,
        Roster_To_Person_Relationship_Inline,
        Association_to_Person_Inline,
        Inactive_Club_to_Person_Inline,
        Inactive_Association_to_Person_Inline,
    )
    actions = ["export_to_csv", "send_conflict_email"]
    ordering = ("firstname", "lastname", "birthdate")

    form = PersonForm

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj=obj)

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj=obj)

    def save_model(self, request, obj, form, change):
        email = form.cleaned_data["email"]
        firstname = form.cleaned_data["firstname"]
        lastname = form.cleaned_data["lastname"]
        birthdate = form.cleaned_data["birthdate"].year

        try:
            user = obj.user
            user.username = f"{birthdate}{lastname}{firstname}"
            user.email = email

        except AttributeError:
            user, _ = User.objects.get_or_create(
                username=f"{birthdate}{lastname}{firstname}", email=email
            )

        user.save()

        obj.user = user
        super().save_model(request, obj, form, change)

    def send_conflict_email(self, request, queryset):
        mail.send_conflict_notification(request, queryset)

    def export_to_csv(self, request, queryset):
        old_queryset = views.PersonViewSet.queryset
        views.PersonViewSet.queryset = queryset

        request.method = "GET"
        request.META["HTTP_ACCEPT"] = "text/csv"

        response = views.PersonViewSet.as_view({"get": "list"})(request)
        views.PersonViewSet.queryset = old_queryset
        return response


class OrganistaionAdmin(customFilteredGuardedModelAdmin):
    list_display = ("name", "image_45p_tag", "founded_on", "members")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ["image_500p_tag"]
    disabled_fields = []

    def get_form(self, *args, **kwargs):
        """ allow diabled_fields for form"""

        form = super().get_form(*args, **kwargs)
        for field_name in self.disabled_fields:
            form.base_fields[field_name].disabled = True
        return form


class AssociationAdmin(OrganistaionAdmin):
    inlines = (
        Member_Association_to_Association_Inline,
        Association_to_Member_Association_Inline,
        Club_to_Association_Inline,
        Person_to_Association_Inline,
        Inactive_Person_to_Association_Inline,
    )

    def members(self, obj):
        return (
            models.ClubToAssociationMembership.objects.filter(association=obj)
            .active()
            .count()
        )


class ClubAdmin(OrganistaionAdmin):
    list_display = OrganistaionAdmin.list_display + ("teams",)
    inlines = (
        Association_To_Club_Inline,
        Person_to_Club_Inline,
        Inactive_Person_to_Club_Inline,
    )
    ordering = ("name",)
    search_fields = ("name",)

    if settings.DEBUG:
        list_display = list_display + ("votes",)

    def members(self, obj):
        return models.PersonToClubMembership.objects.filter(club=obj).active().count()

    def votes(self, obj):
        return math.sqrt(self.members(obj)) * 10

    def teams(self, obj):
        return models.Team.objects.filter(club_membership=obj).count()


class TeamAdmin(OrganistaionAdmin):
    list_display = OrganistaionAdmin.list_display + ("club",)
    inlines = (Roster_Inline,)
    autocomplete_fields = ("club_membership",)

    def club(self, instance):
        if instance.club_membership:
            return instance.club_membership.name
        return None

    def members(self, obj):
        return models.PersonToTeamMembership.objects.filter(team=obj).active().count()


class EventAdmin(CustomGuardedModelAdmin):
    list_display = (
        "name",
        "description",
        "start",
        "end",
    )
    search_fields = list_display
    list_display_links = ("name",)
    # search_fields = ("name","description","start","end",)
    ordering = ("start",)


class TournamentAdmin(EventAdmin):
    inlines = (TournamentDivision_Inline,)


class DivisionAdmin(CustomGuardedModelAdmin):
    list_display = ("name", "description", "eligible_person_query", "eligible_team_query")
    list_display_links = ("name",)
    search_fields = ("name", "description")
    readonly_fields = ["eligible_person_query", "eligible_team_query"]


class TournamentDivisionAdmin(CustomGuardedModelAdmin):
    list_display = ("tournament", "division", "start", "end")
    fields = ("tournament", "division", "start", "end")
    readonly_fields = (
        "start",
        "end",
    )
    # inlines = (Roster_Inline,)
    search_fields = (
        "tournament",
        "division",
    )

    def start(self, obj):
        return obj.tournament.start

    def end(self, obj):
        return obj.tournament.end


class RosterAdmin(customFilteredGuardedModelAdmin):
    list_display = ("name", "team", "tournament_division", "tournament", "division")
    inlines = (Person_To_Roster_Relationship_Inline,)
    search_fields = (
        "team__name",
        "tournament_division__tournament__name",
        "tournament_division__division__name",
    )
    autocomplete_fields = ("team", "persons", "tournament_division")
    list_filter = ("team", "tournament_division")

    def tournament(self, obj):
        return obj.tournament_division.tournament.name

    def division(self, obj):
        return obj.tournament_division.division.name

    def name(self, obj):
        return obj.__str__()


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Association, AssociationAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.Division, DivisionAdmin)
admin.site.register(models.TournamentDivision, TournamentDivisionAdmin)
admin.site.register(models.Roster, RosterAdmin)
