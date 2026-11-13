from django.test import TestCase

# Create your tests here.


from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleAuthViewTests(APITestCase):

    @patch("apps.testapp.views.get_google_user_info")
    @patch("apps.testapp.views.get_google_access_token")
    def test_google_auth_creates_user_and_returns_tokens(
        self, mock_access_token, mock_user_info
    ):
        mock_access_token.return_value = "fake-google-access-token"
        mock_user_info.return_value = {
            "email": "test@example.com",
            "name": "Test User",
        }

        response = self.client.post(
            "/api/v1/testapp/auth/google/",
            {"code": "fake-google-code"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_new_user"])
        self.assertEqual(response.data["user"]["email"], "test@example.com")

        user = User.objects.get(email="test@example.com")
        self.assertFalse(user.has_usable_password())

        refresh = RefreshToken(response.data["tokens"]["refresh"])
        self.assertEqual(refresh["email"], "test@example.com")
        self.assertEqual(refresh["role"], "user")

        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
