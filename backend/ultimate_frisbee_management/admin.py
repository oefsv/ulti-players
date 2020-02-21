import datetime
import math
import sys

from django.contrib import admin
from . import models
from .utils import mail
from datetime import date, timedelta
from django.db.models import Count, Q
from django.conf import settings

from django.contrib.admin.options import ModelAdmin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user, get_objects_for_group, get_perms

# Register your models here..


class MembershipInline(admin.TabularInline):
    model = models.PersonToTeamMembership
    extra = 0
    exclude = ["reporter", "approved_by"]


class Person_to_Team_Inline(MembershipInline):
    model = models.PersonToTeamMembership
    autocomplete_fields = ("person", "team")
    list_filter = autocomplete_fields
    # readonly_fields = ("person","team","role")


class Person_to_Club_Inline(MembershipInline):
    model = models.PersonToClubMembership
    autocomplete_fields = ("person", "club")
    list_filter = autocomplete_fields


class Person_to_Association_Inline(MembershipInline):
    model = models.PersonToAssociationMembership
    autocomplete_fields = ("association", "person")


class Club_to_Association_Inline(MembershipInline):
    model = models.ClubToAssociationMembership
    autocomplete_fields = ("association", "club")


class Association_to_Association_Inline(MembershipInline):
    model = models.AssociationToAssociationMembership
    fk_name = "governor"
    autocomplete_fields = ("member", "governor")
    list_filter = autocomplete_fields


class TournamentDivision_Inline(admin.TabularInline):
    model = models.TournamentDivision
    autocomplete_fields = ("division",)
    extra = 0


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


class Elegible_Nationals(admin.SimpleListFilter):
    title = "Elegible_Nationals"
    parameter_name = "Elegible_Nationals"
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


class PersonAdmin(CustomGuardedModelAdmin):
    list_display = (
        "id",
        "firstname",
        "lastname",
        "image_45p_tag",
        "birthdate",
        "sex",
        "user",
        "eligibile_u17",
        "u20",
        "u24",
        "nationals",
    )
    readonly_fields = ["image_500p_tag"]
    # editable list fields cause huge performance issues when in debug mode
    if not settings.DEBUG:
        list_editable = ("firstname", "lastname", "sex", "birthdate")

    list_filter = (Eligibile_u17, Eligibile_u20, Eligibile_u24, Elegible_Nationals)
    list_display_links = ("id",)
    search_fields = ("firstname", "lastname", "birthdate")
    inlines = (Person_to_Team_Inline, Person_to_Club_Inline, Person_to_Association_Inline)
    actions = ["send_conflict_email"]
    ordering = ("firstname", "lastname", "birthdate")

    def u20(self, obj):
        return obj.eligibile_u20

    u20.boolean = True

    def u24(self, obj):
        return obj.eligibile_u24

    u24.boolean = True

    def nationals(self, instance):
        return instance.eligibile_nationals

    nationals.boolean = True

    def send_conflict_email(self, request, queryset):
        mail.send_conflict_notification(request, queryset)


class OrganistaionAdmin(CustomGuardedModelAdmin):
    list_display = ("name", "image_45p_tag", "founded_on", "dissolved_on", "members")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ["image_500p_tag"]
    disabled_fields = []
    if not settings.DEBUG:
        list_editable = ("founded_on", "dissolved_on")

    def get_queryset(self, request):
        objects = get_objects_for_user(
            user=request.user,
            perms=[f"view_{self.model.__name__.lower()}",],
            klass=self.model,
            accept_global_perms=False,
        )
        return objects

    def get_form(self, *args, **kwargs):
        """ allow diabled_fields for form"""

        form = super().get_form(*args, **kwargs)
        for field_name in self.disabled_fields:
            form.base_fields[field_name].disabled = True
        return form


class AssociationAdmin(OrganistaionAdmin):
    inlines = (Association_to_Association_Inline, Club_to_Association_Inline, Person_to_Association_Inline)

    def members(self, obj):
        return models.ClubToAssociationMembership.objects.filter(association=obj).count()


class ClubAdmin(OrganistaionAdmin):
    list_display = OrganistaionAdmin.list_display + ("teams",)
    inlines = (Club_to_Association_Inline, Person_to_Club_Inline)
    ordering = ("name",)

    if settings.DEBUG:
        list_display = list_display + ("votes",)

    def members(self, obj):
        return models.PersonToClubMembership.objects.filter(club=obj).count()

    def votes(self, obj):
        return math.sqrt(self.members(obj)) * 10

    def teams(self, obj):
        return models.Team.objects.filter(club_membership=obj).count()


class TeamAdmin(OrganistaionAdmin):
    list_display = OrganistaionAdmin.list_display + ("club",)
    inlines = (Person_to_Team_Inline,)

    def club(self, instance):
        if instance.club_membership:
            return instance.club_membership.name
        return None

    def members(self, obj):
        return models.PersonToTeamMembership.objects.filter(team=obj).count()


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


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Association, AssociationAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.Division, DivisionAdmin)
admin.site.register(models.Roster)
