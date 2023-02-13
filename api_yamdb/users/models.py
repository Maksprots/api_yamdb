from api.utils import username_validation
from django.contrib.auth.models import AbstractUser

from django.db import models

USER_ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]
"""Выбор ролей"""


class User(AbstractUser):
    """Кастомная модель User"""

    username = models.CharField(
        max_length=32,
        default='username_default',
        unique=True,
        validators=(username_validation,),
    )
    first_name = models.CharField(
        max_length=32,
        default='user_name_default'
    )
    last_name = models.CharField(
        max_length=64,
        default='user_last_name_default'
    )
    email = models.EmailField(
        verbose_name='email_address',
        blank=False,
        unique=True,
        max_length=254,
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,

    )

    class Meta:
        unique_together = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property  # нужно для удобного доступа
    def is_user(self):  # чтобы не вызывать постоянно функцию
        return self.role == 'user'  # советую почитать про этот декоратор!

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return (self.role == 'admin'
                or self.is_superuser
                or self.is_staff
                )



