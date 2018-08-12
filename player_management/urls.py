from django.urls import path
from django.views import generic
from . import views

app_name = 'player_management'

urlpatterns = [
    path('', views.index,  name='index'),
    #path('', views.IndexView.as_view(),  name='index'),

]