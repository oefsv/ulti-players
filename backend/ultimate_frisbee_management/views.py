from _ast import Import
import datetime

from django.db.models import Q
from django.shortcuts import render
from django.views import generic, View
from django.views.generic.list import ListView
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpRequest, HttpResponse,HttpRequest

from guardian.decorators import permission_required
from guardian.shortcuts import get_perms
from guardian.mixins import LoginRequiredMixin

from rest_framework import permissions, reverse
from rest_framework import viewsets, views
from rest_framework import serializers as restserializers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions


from viewflow.decorators import flow_start_view

from . import serializers
from .serializers import User, GroupSerializer, UserSerializer
from . import models as pm

class DeepLinkView(LoginRequiredMixin,View):
    def get(self, request:HttpRequest,model_name,id, format=None):

        request.user
        model = getattr(pm, model_name)
        instance = model.objects.get(id=id)
       # if f'change_{model_name.lower()}'in get_perms(request.user,instance):
        instance.valid_until = request.GET['valid-until']    
        instance.save()
        return HttpResponse("its done")
      #  else:
      #      return HttpResponseForbidden('you dont have permission (anymore) to do this.')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ultimate_frisbee_management': "http://" + request.get_host() + "/api/ultimate_frisbee_management/", # dont use namespaces with rest framework
        'auth': reverse_lazy('auth_root', request=request),
        'iam': "http://" + request.get_host() + "/api/iam/",
    })


@api_view(['GET'])
def rest_auth_root(request, format=None):
    return Response({
        'login': reverse_lazy('rest_auth:rest_login', request=request),
        'logout': reverse_lazy('rest_auth:rest_logout', request=request),
        'user': reverse_lazy('rest_auth:rest_user_details', request=request),
        'change password': reverse_lazy('rest_auth:rest_password_change', request=request),
        'reset': reverse_lazy('rest_auth:rest_password_reset', request=request),
        'confirm reset': reverse_lazy('rest_auth:rest_password_reset_confirm', request=request),

    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



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

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     response = super().retrieve(request, *args, **kwargs)
    #     dict = {
    #         'hit': response.data,
    #     }
    #    # association_memberships=
    #     dict["teams"] = reverse.reverse_lazy("persontoassociationmembership-list",request=request)
    #     return Response(dict)



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

    @flow_start_view
    def create(self, request, *args, **kwargs):
        super(PersonToClubMembershipViewSet, self).create()


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