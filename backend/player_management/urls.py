from django.urls import path
from django.views import generic
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from player_management import views

app_name = 'player_management'

router = routers.DefaultRouter()
router.register('persons', views.PersonViewSet)
router.register('persontoassociationmemberships', views.PersonToAssociationMembershipViewSet)

urlpatterns = [
    path('', views.index,  name='index'),
    path('api/', include(router.urls)),

]