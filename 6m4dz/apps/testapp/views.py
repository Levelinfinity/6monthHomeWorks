from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GoogleAuthSerializer
from .services import get_google_access_token, get_google_user_info

# Create your views here.



class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        access_token = get_google_access_token(code)
        google_user = get_google_user_info(access_token)

        email = google_user['email'].strip().lower()
        name = google_user.get('name', '').strip()

        try:
            with transaction.atomic():
                user = User.objects.filter(email__iexact=email).first()
                is_new_user = user is None

                if is_new_user:
                    username = email.split('@')[0][:150]

                    if User.objects.filter(username=username).exists():
                        import uuid
                        username = f"{username}_{uuid.uuid4().hex[:8]}"

                    user = User.objects.create_user(
                        username=username,
                        email=email,
                    )
                    user.set_unusable_password()
                    user.save(update_fields=['password'])

        except IntegrityError:
            user = User.objects.filter(email__iexact=email).first()

            if user is None:
                raise AuthenticationFailed('Не удалось создать пользователя')

            if_new_user = False

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["role"] = "user"

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": name,
                },
                "is_new_user": is_new_user,
                "tokens" : {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )