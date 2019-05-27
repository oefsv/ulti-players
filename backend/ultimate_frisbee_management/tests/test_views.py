from django.contrib.auth.models import User
from rest_auth.views import UserDetailsView
from rest_auth.serializers import UserDetailsSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.reverse import reverse_lazy
from rest_framework import status
from mixer.backend.django import mixer

class TestViews(APITestCase):
    def setUp(self):
        self.factory: APIRequestFactory = APIRequestFactory()

    def test_get_user_profile(self):

        view = UserDetailsView()
        user = mixer.blend(User)

        path = reverse_lazy('rest_auth:rest_user_details')
        request = self.factory.get(path)
        request.user = user
        response = view.dispatch(request)

        serializer = UserDetailsSerializer(user)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == serializer.data['pk']

