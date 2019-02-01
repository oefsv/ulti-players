from _ast import Import
import datetime
from urllib.request import Request

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpRequest, HttpResponse
from rest_framework import viewsets, views
from .serializers import User, GroupSerializer, UserSerializer
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.http.response import JsonResponse


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
