from django.db.models.signals import post_save 
from django.dispatch import receiver
from ..models import PersonToClubMembership,Club,Person,ClubToAssociationMembership,Association
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import User, Group
from itertools import chain

permissions= {

    "club":{
        "admin": {
            Club:['change','delete','view',],
            ClubToAssociationMembership: ['view','delete'],
            Association: ['view'],
            Person: ['view'],
            PersonToClubMembership:['add','delete','view','change'],

        },
    }
}

@receiver(post_save,sender=PersonToClubMembership)
def assign(sender, instance: PersonToClubMembership, **kwargs):

    club = instance.club
    instances = [instance, club]
    instances += club.associations_memberships.all()
    instances.append(ClubToAssociationMembership.objects.get(club=club))
    instances += club.member_persons.all()
    instances += PersonToClubMembership.objects.filter(club=club)

    for role,model_permissions in permissions['club'].items():
        group = Group.objects.get_or_create(name=f"club_{role}_{instance.club.name}")[0]

        for obj in instances:
            for permission in model_permissions[obj.__class__]:
                p = f"{permission}_{obj.__class__.__name__.lower()}"
                assign_perm(p,group,obj)
