"""ultimate_frisbee_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import unicode_literals

from django.urls import path
from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url, include, static
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from django.views.static import serve

app_name = 'ultimate_frisbee_management'

ultimate_frisbee_management_router = routers.DefaultRouter() # todo change the view so its not called "API Root" https://stackoverflow.com/questions/17496249/in-django-restframework-how-to-change-the-api-root-documentation
ultimate_frisbee_management_router.register('PersonalClubs', views.PersonalClubViewset, 'personal-clubs')
ultimate_frisbee_management_router.register('persons', views.PersonViewSet)
ultimate_frisbee_management_router.register('associations', views.AssociationViewSet)
ultimate_frisbee_management_router.register('clubs', views.ClubViewSet)
ultimate_frisbee_management_router.register('teams', views.TeamViewSet)
ultimate_frisbee_management_router.register('personToAssociationMemberships', views.PersonToAssociationMembershipViewSet)
ultimate_frisbee_management_router.register('personToClubMemberships', views.PersonToClubMembershipViewSet)
ultimate_frisbee_management_router.register('personToTeamMemberships', views.PersonToTeamMembershipViewSet)
ultimate_frisbee_management_router.register('clubToAssociationMemberships', views.ClubToAssociationMembershipViewSet)
ultimate_frisbee_management_router.register('AssociationToAssociationMemberships', views.AssociationToAssociationMembershipViewSet)

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)


admin.site.site_header = "ULTIMATE_FRISBEE_MANAGEMENT Admin Portal"
admin.site.site_title = "ULTIMATE_FRISBEE_MANAGEMENT Admin Portal"
admin.site.index_title = "ULTIMATE_FRISBEE_MANAGEMENT Admin Portal"

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


urlpatterns = [

    path('',admin.site.urls,name="admin"),
    path('api/', views.api_root),  # root api view. routes to the submodules
    path('api/auth/', views.rest_auth_root,name="auth_root"), # hack because rest-auth does not provide root view
    path('api/auth/', include(('rest_auth.urls','rest_auth'), namespace="rest_auth")),
    path('api/iam/',  include(router.urls)),  # identity and access management users, groups etc..
    path('api/ultimate_frisbee_management/',  include(ultimate_frisbee_management_router.urls)),
    path('deeplink/<str:model_name>/<int:id>/',views.DeepLinkView.as_view()),
    path('pdf/<str:template>',views.GeneratePdf.as_view()),
    path('tmp/<str:template>',views.dummyHtml.as_view()),
] + static.static(settings.MEDIA_URL,view=protected_serve, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        #url(r'^silk/', include('silk.urls', namespace='silk'))
    ] + urlpatterns