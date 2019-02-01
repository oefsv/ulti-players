from django.urls import path
from django.views import generic
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from player_management import views

app_name = 'player_management'

router = routers.DefaultRouter() # todo change the view so its not called API Root https://stackoverflow.com/questions/17496249/in-django-restframework-how-to-change-the-api-root-documentation
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

association_detail = views.AssociationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
club_detail = views.ClubViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
team_detail = views.TeamViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
person_detail = views.PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', views.index,  name='index'),
    path('api/', include(router.urls)),
    path('association/<int:pk>/', association_detail, name='association-detail'),
    path('club/<int:pk>/', club_detail, name='club-detail'),
    path('team/<int:pk>/', team_detail, name='team-detail'),
    path('person/<int:pk>/', person_detail, name='person-detail'),
]