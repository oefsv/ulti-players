from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import PersonToClubMembership,Club,Person,ClubToAssociationMembership,Association,Team,PersonToTeamMembership
from django.contrib.auth.models import User, Group
from itertools import chain
from guardian.shortcuts import assign_perm

permissions= {

    "club":{
        "admin": {
            Club:['change','delete','view',],
            ClubToAssociationMembership: ['view','delete'],
            Association: ['view'],
            Person: ['view'],
            PersonToClubMembership:['add','delete','view','change'],
            Team:['add','delete','view','change'],
            PersonToTeamMembership:['add','delete','view','change'],
        },
    },
    "team":{
        "admin": {
            Person: ['view'],
            Team:['add','delete','view','change'],
            PersonToTeamMembership:['add','delete','view','change'],
        },
    },
    
}

def assign_permissions_based_on_membership(instances, permission_source_obj):
    permission_prefix= permission_source_obj.__class__.__name__.lower()

    if permission_prefix in permissions:
        for role,model_permissions in permissions[permission_prefix].items():
            group = Group.objects.get_or_create(name=f"{permission_prefix}_{role}_{permission_source_obj.name}")[0]

            for obj in instances:
                for permission in model_permissions[obj.__class__]:
                    p = f"{permission}_{obj.__class__.__name__.lower()}"
                    assign_perm(p,group,obj)

def delete_permissions_for_organisation(instances, permission_source_obj):
    permission_prefix= permission_source_obj.__class__.__name__.lower()

    for role,model_permissions in permissions[permission_prefix].items():
        group = Group.objects.get_or_create(name=f"{permission_prefix}_{role}_{permission_source_obj.name}")[0]
        group.delete()


@receiver(post_save,sender=PersonToClubMembership)
def assign_permissions_based_on_club_membership(sender, instance: PersonToClubMembership, **kwargs):

    club = instance.club
    instances = [instance, club]
    instances += club.associations_memberships.all()
    instances += ClubToAssociationMembership.objects.filter(club=club)
    instances += club.member_persons.all()
    instances += PersonToClubMembership.objects.filter(club=club)

    assign_permissions_based_on_membership(instances,club)



@receiver(post_save,sender=Team)
@receiver(post_save,sender=Club)
@receiver(post_save,sender=Association)
def create_permissions_group_for_Organisation(sender, instance, **kwargs):
    assign_permissions_based_on_membership([instance],instance)

@receiver(post_delete,sender=Team)
@receiver(post_delete,sender=Club)
@receiver(post_delete,sender=Association)
def delete_permissions_group_for_Organisation(sender, instance, **kwargs):
    delete_permissions_for_organisation([instance],instance)


@receiver(post_save,sender=PersonToTeamMembership)
def assign_permissions_based_on_team_membership(sender, instance: PersonToTeamMembership, **kwargs):

    team = instance.team
    instances = [instance, team]
    instances += team.member_persons.all()
    instances += PersonToTeamMembership.objects.filter(team=team)

    assign_permissions_based_on_membership(instances,team)