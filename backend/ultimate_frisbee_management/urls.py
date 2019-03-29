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

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)


urlpatterns = [

    path('',views.api_root),
    path('api/', views.api_root),  # root api view. routes to the submodules
    path('api/auth/', views.rest_auth_root,name="auth_root"), # hack because rest-auth does not provide root view
    path('api/auth/', include(('rest_auth.urls','rest_auth'), namespace="rest_auth")),
    path('api/iam/',  include(router.urls)),  # identity and access management users, groups etc..
    path('api/player_management/', include('player_management.urls')), # player management
    path('admin/', admin.site.urls, name='admin'),
]
