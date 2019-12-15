from django.contrib import admin
from . import models
from .utils import mail
import datetime
from datetime import date,timedelta
from django.db.models import Count, Q
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user,get_objects_for_group
# Register your models here..


class MembershipInline(admin.TabularInline):
    model = models.PersonToTeamMembership
    extra = 1
    exclude = ['reporter','approved_by']
    list_filter = ('country', )

class Person_to_Team_Inline(MembershipInline):
    model = models.PersonToTeamMembership
    raw_id_fields = ("person","team")
    list_filter = raw_id_fields

class Person_to_Club_Inline(MembershipInline):
    model = models.PersonToClubMembership
    raw_id_fields = ("person","club")
    list_filter = raw_id_fields

class Person_to_Association_Inline(MembershipInline):
    model = models.PersonToAssociationMembership
    raw_id_fields = ("association","person")
    list_filter = raw_id_fields

class Club_to_Association_Inline(MembershipInline):
    model = models.ClubToAssociationMembership
    raw_id_fields = ("association","club")

class Association_to_Association_Inline(MembershipInline):
    model = models.AssociationToAssociationMembership
    fk_name = 'governor'
    raw_id_fields = ("member","governor")
    list_filter = raw_id_fields


class BaseFilter(admin.SimpleListFilter):
    title = 'eligibile'
    parameter_name = 'eligibile'
    age = 0

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        startdate = date.today() + timedelta(days=-self.age*365)
        enddate = date.today()
        if value == 'Yes':
            return queryset.filter(birthdate__range=[startdate, enddate])
        elif value == 'No':
            return queryset.exclude(birthdate__range=[startdate, enddate])
        return queryset

class Eligibile_u17(BaseFilter):
    title = 'Eligibile_u17' 
    parameter_name = 'Eligibile_u17'
    age=17
class Eligibile_u20(BaseFilter):
    title = 'Eligibile_u20'
    parameter_name = 'Eligibile_u20'
    age=20
class Eligibile_u24(BaseFilter):
    title = 'Eligibile_u24'
    parameter_name = 'Eligibile_u24'
    age=24

class Elegible_Nationals(admin.SimpleListFilter):
    title = 'Elegible_Nationals'
    parameter_name = 'Elegible_Nationals'
    age = 0

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        today = date.today()
        this_year = date(year=today.year, month=1, day=1)
        if value == 'Yes':
            return queryset.filter(Q(persontoclubmembership__valid_until__gte=this_year)|Q(persontoclubmembership__valid_until__isnull=True)).annotate(clubs_count=Count('club_memberships')).filter(clubs_count__lt=2)
        elif value == 'No':
            return queryset.filter(Q(persontoclubmembership__valid_until__gte=this_year)|Q(persontoclubmembership__valid_until__isnull=True)).annotate(clubs_count=Count('club_memberships')).filter(clubs_count__gte=2)
        return queryset

class PersonAdmin(GuardedModelAdmin):
    list_display = ('id','firstname', 'lastname', 'birthdate','sex', 'user',
        'eligibile_u17','eligibile_u20','eligibile_u24','elegible_nationals')
    #list_editable = ('firstname', 'lastname', 'sex',)
    list_filter = (Eligibile_u17,Eligibile_u20,Eligibile_u24,Elegible_Nationals)  
    list_display_links = ('id',)
    search_fields = ('firstname','lastname')
    inlines = (Person_to_Team_Inline,Person_to_Club_Inline,Person_to_Association_Inline)
    actions = ['send_conflict_email']


    def eligibile_u17(self, obj):
        return obj.eligibile_u17
    eligibile_u17.boolean=True

    def elegible_nationals(self, instance):
        return instance.eligibile_nationals
    elegible_nationals.boolean= True

    def send_conflict_email(self, request, queryset):
        mail.send_conflict_notification(request,queryset)


class OrganistaionAdmin(GuardedModelAdmin):
    list_display = ('id','name','founded_on', 'dissolved_on',)
    list_display_links = ('id',)
    
    def get_queryset(self, request):
        objects = get_objects_for_user(user=request.user, perms=[f'view_{self.model.__name__.lower()}', ], klass=self.model,accept_global_perms=False)
        return objects
   # list_editable = ('name','founded_on','dissolved_on',)

        def get_form(self, *args, **kwargs):
            """ allow diabled_fields for form"""
        form = super(ClubAdmin, self).get_form(*args, **kwargs)
        for field_name in self.disabled_fields:
            form.base_fields[field_name].disabled = True
        return form



class AssociationAdmin(OrganistaionAdmin):
    inlines = (Association_to_Association_Inline,Club_to_Association_Inline,Person_to_Association_Inline)


class ClubAdmin(OrganistaionAdmin):
    inlines = (Club_to_Association_Inline,Person_to_Club_Inline)
    fake_readonly_fields = ("name",)
    
    def get_form(self, *args, **kwargs):
        form = super(ClubAdmin, self).get_form(*args, **kwargs)
        for field_name in self.fake_readonly_fields:
            form.base_fields[field_name].disabled = True
        return form

class TeamAdmin(OrganistaionAdmin):
    list_display = OrganistaionAdmin.list_display +('club',)
    inlines = (Person_to_Team_Inline,)

    def club(self, instance):
        if instance.club_membership:
            return instance.club_membership.name
        return None

    


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Association, AssociationAdmin)
admin.site.register(models.Club,ClubAdmin)
admin.site.register(models.Team,TeamAdmin)
