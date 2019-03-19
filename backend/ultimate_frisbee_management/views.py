from _ast import Import
import datetime
from urllib.request import Request

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpRequest, HttpResponse
from rest_framework import viewsets, views
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse, reverse_lazy


from .serializers import User, GroupSerializer, UserSerializer
from rest_framework import permissions

from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'player_management': "http://" + request.get_host() + "/api/player_management/", # dont use namespaces with rest framework
        'auth': reverse_lazy('auth_root', request=request),
        'iam': "http://" + request.get_host() + "/api/iam/",
    })

@api_view(['GET'])
def rest_auth_root(request, format=None):
    return Response({
        'login': reverse_lazy('rest_auth:rest_login', request=request),
        'logout': reverse_lazy('rest_auth:rest_logout', request=request),
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