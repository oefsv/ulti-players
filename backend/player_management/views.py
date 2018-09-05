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
from player_management.serializers import PersonSerializer
from rest_framework import permissions


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = pm.Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated,)