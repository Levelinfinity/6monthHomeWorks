
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def google_auth_service(code: str) -> dict:

    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth не настроен.")

    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data=payload,
            timeout=10
        )
        token_response.raise_for_status()
        token_data = token_response.json()

        access_token = token_data.get("access_token")

        if not access_token:
            raise ValueError("Google не вернул access token.")

        user_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        user_response.raise_for_status()
        user_data = user_response.json()

    except requests.RequestException as exc:
        raise ValueError("Ошибка соединения с Google.") from exc

    email = user_data.get("email")

    if not email or user_data.get("verified_email") is not True:
        raise ValueError("Google email не подтверждён.")

    email = User.objects.normalize_email(email.strip()).lower()

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "role": User.Role.STUDENT,
            "first_name": user_data.get("given_name", ""),
            "last_name": user_data.get("family_name", ""),
        }
    )

    if not user.is_active:
        raise ValueError("Пользователь отключён.")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "is_new_user": created,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }
