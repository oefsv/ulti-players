from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView

from . import serializers
from . import models as pm
from rest_framework import permissions, reverse
from rest_framework import viewsets
from rest_framework import serializers as restserializers


# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


def index(response):
    return HttpResponse("Hello, world. You're at the frisbee index.")


class IndexView(generic.TemplateView):
    template_name = 'player_management/index.html'




class managedClubViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows Clubs to be viewed or edited that the.
    current user is managing. it filters out all the clubs the person is managing
    """
    serializer_class = serializers.ClubSerializer
    def get_queryset(self):
        user = self.request.user
        person = pm.Club.objects.filter(~Q(persontoclubmembership__role = 'member'), persontoclubmembership__person__user=user)

        return person

class PersonalClubViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows Clubs to be viewed or edited that the.
    current user is managing.
    """
    serializer_class = serializers.ClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        person = pm.Club.objects.filter(persontoclubmembership__person__user=user)
        return person


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Person to be viewed or edited.
    """
    queryset = pm.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        dict = {
            'hit': response.data,
        }
       # association_memberships=
        dict["teams"] = reverse.reverse_lazy("player_management:persontoassociationmembership-list",request=request)
        return Response(dict)




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