import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()

def google_auth_service(code: str) -> dict:
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code',
    }

    token_response = requests.post(token_url, data=payload)
    token_data = token_response.json()

    if 'access_token' not in token_data:
        raise ValueError(f"Ошибка обмена кода с Google: {token_data}")

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    user_data = userinfo_response.json()

    email = user_data.get('email')
    if not email:
        raise ValueError("Google профиль не содержит email.")

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'role': User.Role.STUDENT,
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
        }
    )

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