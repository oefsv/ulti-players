from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http import HttpResponse

def index(response):
    return HttpResponse("Hello, world. You're at the frisbee index.")


class IndexView(generic.TemplateView):
    template_name = 'player_management/index.html'


import player_management.models as pm
from rest_framework import viewsets
from player_management import serializers
from rest_framework import permissions




class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    # permission_classes = (permissions.IsAuthenticated,)

class AssociationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.Association.objects.all()
    serializer_class = serializers.AssociationSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.Club.objects.all()
    serializer_class = serializers.ClubSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    # permission_classes = (permissions.IsAuthenticated,)



class PersonToAssociationMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.PersonToAssociationMembership.objects.all()
    serializer_class = serializers.PersonToAssociationMembershipSerializer


class PersonToClubMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.PersonToClubMembership.objects.all()
    serializer_class = serializers.PersonToClubMembershipSerializer


class PersonToTeamMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.PersonToTeamMembership.objects.all()
    serializer_class = serializers.PersonToTeamMembershipSerializer


class ClubToAssociationMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.ClubToAssociationMembership.objects.all()
    serializer_class = serializers.ClubToAssociationMembershipSerializer


class AssociationToAssociationMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.AssociationToAssociationMembership.objects.all()
    serializer_class = serializers.AssociationToAssociationMembershipSerializer