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
from guardian.ctypes import get_content_type


def set_permissions(granting_class, role, permission_target, granting_objects_selector, permissions=["view"]):
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
    granting_objects = granting_objects_selector(permission_target)
    target_class_name = permission_target.__class__.__name__.lower()
    granting_class_name = granting_class.__name__.lower()

    # delete all permission for current target, role and granting class
    old_permissions = GroupObjectPermission.objects.filter(
        Q(group__name__startswith=f"{ granting_class_name}_{role}")
        & Q(object_pk=permission_target.pk)
        & Q(content_type=get_content_type(permission_target))
    )
    old_permissions.delete()

    if isinstance(granting_objects, granting_class):
        granting_object_names_list = [granting_objects.name]
    else:
        granting_object_names_list = granting_objects.values_list("name", flat=True)

    groups_names = [
        Group.objects.get_or_create(name=f"{granting_class_name}_{role}_{name}")[0].name
        for name in granting_object_names_list
    ]
    groups = Group.objects.filter(name__in=groups_names)

    for perm in permissions:
        assign_perm(f"{perm}_{target_class_name}", groups, permission_target)


def get_permission_assigner(granting_class, role, granting_objects_selector, permissions=["view"]):
    """ return a function that just needs the target object
    on which permissions are granted
    """
    return lambda permission_target: set_permissions(
        granting_class, role, permission_target, granting_objects_selector, permissions
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
            Club: {"selector": lambda club: club, "permissions": ["view"]},
            Association: {
                "selector": lambda association: Club.objects.filter(associations_memberships__pk=association.pk),
                "permissions": ["view"],
            },
            ClubToAssociationMembership: {
                "selector": lambda membership: membership.club,
                "permissions": ["view", "delete"],
            },
            Person: {
                "selector": lambda person: Club.objects.filter(member_persons__pk=person.pk),
                "permissions": ["view"],
            },
            PersonToClubMembership: {
                "selector": lambda membership: membership.club,
                "permissions": ["add", "delete", "view", "change"],
            },
            Team: {"selector": lambda team: team.club_membership, "permissions": ["add", "delete", "view", "change"]},
            Roster: {
                "selector": lambda roster: roster.team.club_membership,
                "permissions": ["add", "delete", "change", "view"],
            },
            PersonToRosterRelationship: {
                "selector": lambda relationship: relationship.roster.team.club_membership,
                "permissions": ["add", "delete", "view", "change"],
            },
            Tournament: {"selector": lambda tournament: Club.objects.all(), "permissions": ["view"]},
            TournamentDivision: {"selector": lambda tournamentDivision: Club.objects.all(), "permissions": ["view"]},
        },
    }
}

# construct a more efficient map based on the permission_target and a list
# of functions that assign permissions if an instance of permissio_target ist
# updated

grant_permissions_for_target = {}
for granting_class, roles in permissions.items():
    for role, target_classes in roles.items():
        for target_class, params in target_classes.items():
            grant_permissions_for_target.setdefault(target_class, []).append(
                get_permission_assigner(
                    granting_class=granting_class,
                    role=role,
                    granting_objects_selector=params["selector"],
                    permissions=params["permissions"],
                )
            )


@receiver([post_save, post_delete])
def update_permissions_based_on_granting_objects_and_roles(sender, instance, **kwargs):
    if sender in grant_permissions_for_target.keys():

        # TODO: if permission is granted for all objects of class, create global permission
        for update_permissions in grant_permissions_for_target[sender]:
            update_permissions(instance)
