from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver
from ..models import (
    PersonToClubMembership,
    Club,
    Person,
    ClubToAssociationMembership,
    Association,
    Team,
    PersonToTeamMembership,
    Division,
    Tournament,
    TournamentDivision,
    Roster,
    PersonToRosterRelationship,
)
from django.contrib.auth.models import User, Group
from itertools import chain
from guardian.shortcuts import assign_perm
from guardian.models import GroupObjectPermission
from typing import List, Callable

from django.db.models import Q, QuerySet


def set_permissions(granting_class, role, permission_target, granting_objects, permissions=["view"]):
    """    
    gets a Queryset for groups
    based on the role and the granting class which define the prefix of the group name
    and the target Q object which define the filter for the instances of granting objects
    which make the second part of the group name

    Example: set_permissions(Club,"admin",association, lambda x: Q(associations_memberships_contains=x))
        will grant view permission to to the Club_admin group for every club
        that has association in the list of association_memberships.


    Arguments:
        granting_class {[Class]} -- The Class that grants the permission in example Club
        role {[type]} -- The role on the granting_class object example Admin
        permission_target {[type]} -- the object on which permissions are granted.  example Team
        granting_objects {[type]} -- an instance or Queryset on granting_class

    Keyword Arguments:
        permissions {list} -- list of Permissions on permission_target (default: {["view"]})
    """ 

    if isinstance(granting_objects, granting_class):
        granting_object_names_list = [granting_objects.name]
    else:
        granting_object_names_list = granting_objects.values_list('name', flat=True)

    group_names = [f"{role}_{name}" for name in granting_object_names_list]
    groups = Group.objects.filter(name__in=group_names)

    for perm in permissions:
        assign_perm(perm, groups, permission_target)


def get_permission_assigner(granting_class, role, filter_on_target, permissions=["view"]):
    """ return a function that just needs the target object
    on which permissions are granted
    """
    return lambda permission_target: set_permissions(
        granting_class, 
        role, 
        permission_target, 
        filter_on_target,
        permissions
    )


permissions = {
    # "base": {
    #     Association: ["view"],
    #     Club: ["view"],
    #     ClubToAssociationMembership: ["view",],
    #     Tournament: ["view"],
    #     TournamentDivision: ["view"],
    #     PersonToClubMembership: ["view"],
    #     Team: ["view"],
    #     Roster: ["view"],
    #     PersonToRosterRelationship: ["view"],
    # },
    Club: {
        "admin": {
            Club: {
                "selector": lambda club: club,
                "permissions": ["view"],
            },
            Association: {
                "selector": lambda association: Club.objects.filter(associations_memberships_contains=association),
                "permissions": ["view"],
            },
            ClubToAssociationMembership: {
                "selector": lambda membership: membership.club,
                "permissions": ["view", "delete"],
            },
            Person: {
                "selector": lambda person: Club.objects.filter(member_persons__contains=person),
                "permissions": ["view"],
            },
            PersonToClubMembership: {
                "selector": lambda membership: membership.club,
                "permissions": ["add", "delete", "view", "change"],
            },
            Team: {
                "selector": lambda team: team.club_membership,
                "permissions": ["add", "delete", "view", "change"],
            },
            Roster: {
                "selector": lambda roster: roster.team.club_membership,
                "permissions": ["add", "delete", "view", "change"],
            },
            PersonToRosterRelationship: {
                "selector": lambda relationship: relationship.roster.team.club_membership,
                "permissions": ["add", "delete", "view", "change"],
            },
            Tournament: {
                "selector": lambda tournament: Club.objects.all(),
                "permissions": ["view"],
            },
            TournamentDivision: {
                "selector": lambda tournamentDivision: Club.objects.all(),
                "permissions": ["view"],
            },
        },
    }
}

#construct a more efficient map based on the permission_target and a list
#of functions that assign permissions if an instance of permissio_target ist
# updated 

permissions_inverted = {}
for granting_class, role in permissions.items():
    for target_oject, params in role:
        permissions_inverted[target_oject] += [
            get_permission_assigner(
                granting_class=granting_class,
                role=role,
                granting_objects=params["selector"],
                permissions=params["permissions"])
            ]


def get_permission_targets_for_role_based_on_object(role: str, obj: models.Model) -> list:

    instances = []
    if role == "admin" and isinstance(obj, Club):
        club: Club = obj
        instances += [club]  # Has access to club itself
        instances += club.associations_memberships.all()  # add all associated Association
        instances += ClubToAssociationMembership.objects.filter(club=club)  # add all memberships associated with club
        instances += club.member_persons.all()  # all club members
        instances += PersonToClubMembership.objects.filter(club=club)  # all club memberships
        instances += Team.objects.filter(club_membership=club)
        instances += Roster.objects.filter(team__club_membership=club)
        instances += PersonToRosterRelationship.objects.filter(roster__team__club_membership=club)  # can see and edit
        instances += Tournament.objects.all()  # can see all tournaments
        instances += TournamentDivision.objects.all()  # can see all tournament divisions
    return instances


def update_object_permissions_for_group(role: str, role_granting_object):
    """updates all object_level permissions based on role

    Arguments:
        role {str} -- the role that recieves the permissions
    """
    class_name = role_granting_object.__class__.__name__.lower()
    permission_roles = permissions.get(role_granting_object.__class__)

    #  if permissions dictionary has a permission model based on the object class (example "club")
    if permission_roles is not None:
        # for each role get its permission sets
        for role_name, role_permissions in permission_roles.items():

            # create or fetch a group for the role
            group = Group.objects.get_or_create(name=f"{class_name}_{role}_{role_granting_object.name}")[0]

            # remove all existing permissions for group
            # TODO: optimize this
            GroupObjectPermission.objects.filter(group=group).delete()

            # get all objects for which the permissions should be set
            objects = get_permission_targets_for_role_based_on_object(role=role_name, obj=role_granting_object)

            # assign all permission to objects based on
            for obj in objects:
                class_permissions = role_permissions.get(obj.__class__)
                if class_permissions is not None:
                    for permission in role_permissions[obj.__class__]:
                        p = f"{permission}_{obj.__class__.__name__.lower()}"
                        assign_perm(p, group, obj)


def delete_permissions_for_organisation(instances, permission_source_obj):
    permission_prefix = permission_source_obj.__class__.__name__.lower()

    for role, model_permissions in permissions[permission_prefix].items():
        group = Group.objects.get_or_create(name=f"{permission_prefix}_{role}_{permission_source_obj.name}")[0]
        group.delete()


@receiver(post_save, sender=PersonToClubMembership)
def assign_permissions_based_on_club_membership(sender, instance: PersonToClubMembership, **kwargs):

    club = instance.club
    instances = [instance, club]
    instances += club.associations_memberships.all()
    instances += ClubToAssociationMembership.objects.filter(club=club)
    instances += club.member_persons.all()
    instances += PersonToClubMembership.objects.filter(club=club)

    update_object_permissions_for_group(instances, club)


@receiver(post_save, sender=Team)
@receiver(post_save, sender=Club)
@receiver(post_save, sender=Association)
@receiver(post_save, sender=Roster)
def create_permissions_group_for_Organisation(sender, instance, **kwargs):
    update_object_permissions_for_group("admin", instance)


@receiver(post_delete, sender=Team)
@receiver(post_delete, sender=Club)
@receiver(post_delete, sender=Association)
@receiver(post_delete, sender=Roster)
def delete_permissions_group_for_Organisation(sender, instance, **kwargs):
    delete_permissions_for_organisation("admin", instance)


@receiver(post_save, sender=PersonToTeamMembership)
def assign_permissions_based_on_team_membership(sender, instance: PersonToTeamMembership, **kwargs):

    team = instance.team
    instances = [instance, team]
    instances += team.member_persons.all()
    instances += PersonToTeamMembership.objects.filter(team=team)

    update_object_permissions_for_group(instances, team)

