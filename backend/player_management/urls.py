from django.urls import path
from django.views import generic
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from . import views

app_name = 'player_management'

router = routers.DefaultRouter() # todo change the view so its not called "API Root" https://stackoverflow.com/questions/17496249/in-django-restframework-how-to-change-the-api-root-documentation
router.register('PersonalClubs', views.PersonalClubViewset, 'Clubs')
router.register('persons', views.PersonViewSet)
router.register('associations', views.AssociationViewSet)
router.register('clubs', views.ClubViewSet)
router.register('teams', views.TeamViewSet)
router.register('personToAssociationMemberships', views.PersonToAssociationMembershipViewSet)
router.register('personToClubMemberships', views.PersonToClubMembershipViewSet)
router.register('personToTeamMemberships', views.PersonToTeamMembershipViewSet)
router.register('clubToAssociationMemberships', views.ClubToAssociationMembershipViewSet)
router.register('AssociationToAssociationMemberships', views.AssociationToAssociationMembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]