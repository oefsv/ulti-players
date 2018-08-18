from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.http import HttpResponse

def index(response):
    return HttpResponse("Hello, world. You're at the frisbee index.")


class IndexView(generic.TemplateView):
    template_name = 'player_management/index.html'
