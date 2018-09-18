from _ast import Import
import datetime
from urllib.request import Request

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = User
    permission_classes = (permissions.IsAuthenticated,)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        serializer = User(instance=token.user,context={'request': request})
        return Response({'token': token.key, 'user': serializer.data})


@csrf_exempt
def startSession(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        request.session.set_expiry(86400)  # sets the exp. value of the session
        response = HttpResponse("logged in.")
        serializer = UserSerializer(user, context={'request': request})
        set_cookie(response,'user', serializer.data)
        set_cookie(response, 'session_id', request.session.session_key )
        return response
    else:
        # Show an error page
        return HttpResponseRedirect("/invalid")


def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)