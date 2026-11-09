from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'role': getattr(self.user, 'role', 'client'),
        })
        return data