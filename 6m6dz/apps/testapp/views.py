from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.testapp.serializers import RegisterSerializer
from apps.testapp.tasks import send_welcome_email_task


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            send_welcome_email_task.delay(user.email)

            return Response(
                {
                    "message": "Пользователь успешно зарегистрирован!",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )