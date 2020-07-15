import logging
from typing import Dict, Sequence

from django.contrib.auth.models import User, Group
from django.test import TestCase, client

# Create your tests here.
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status


from django.conf import settings
from django.urls import URLResolver, URLPattern, exceptions
from django.core.mail import send_mail
from django.test.utils import override_settings


logger = logging.getLogger(__name__)

root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
VIEW_NAMES = []  # maintain a global list

detail_views_list = []


def get_all_view_names(urlpatterns, namespace=None):
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            if hasattr(pattern, "namespace") and pattern.namespace is not None:
                namespace = pattern.namespace
            get_all_view_names(pattern.url_patterns, namespace)
        elif isinstance(pattern, URLPattern):
            if pattern.name is not None:
                name = pattern.name
                if namespace is not None:
                    name = namespace + ":" + name
                detail_views_list.append(name)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
class TestEmailVerification(TestCase):
    send_mail(
        "test_email_simple from django",
        "Here is the message.",
        "db-ultimate@frisbeeverband.at",
        ["flokain11@gmail.com"],
    )


class testApiStartSession(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.groups: Dict[Group] = {}
        self.groups["club_admin"] = Group.objects.get_or_create(name="club_admin")
        self.groups["association_admin"] = Group.objects.get_or_create(name="association_admin")

        self.users = {}
        self.users["admin"] = User.objects.create(
            username="admin", email="admin@admin.com", password="admin", is_superuser=True
        )

        self.users["club_admin"] = User.objects.create(
            username="club_admin", email="club-admin@club-admin.com", password="club_admin"
        )

    def test_Session_Start(self):
        response = self.client.post(
            "/api/auth/login/", {"email": "admin@admin.com", "password": "admin"}, format="json"
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_all_urlpatterns(self):

        all_urlpatterns = __import__(settings.ROOT_URLCONF).urls.urlpatterns
        get_all_view_names(all_urlpatterns)
        all_views_list = []

        # remove redundant entries and specific ones we don't care about
        for each in detail_views_list:
            if each not in "serve add_view change_view changelist_view history_view delete_view RedirectView":
                if each not in all_views_list:
                    all_views_list.append(each)

        print(all_views_list)
        for view in all_views_list:
            try:
                response = self.client.get(reverse_lazy(view))
                logger.debug(response.status_code)
                self.assertTrue(
                    status.is_success(response.status_code)
                    or response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
                )
            except exceptions.NoReverseMatch:
                pass
