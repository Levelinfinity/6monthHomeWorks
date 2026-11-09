from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Администратор'
        MANAGER = 'MANAGER', 'Менеджер'
        CLIENT = 'CLIENT', 'Клиент'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CLIENT,
    )

    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']