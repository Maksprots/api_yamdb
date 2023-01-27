import re
from random import randint

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError


def get_confirmation_code():
    """Генерирует 6-тизначный код."""
    return randint(
        settings.CONFIRMATION_CODE_MIN_VALUE,
        settings.CONFIRMATION_CODE_MAX_VALUE
    )


def send_confirmation_code(user):
    """
    Отправляет код для регистрации на почту.
    В качестве аргумента принимает проверенные данные сериализатора
    и объект пользователя.
    """
    send_mail(
        subject='Регистрация на Yamdb',
        message=(
            'Для завершения регистрации на Yamdb отправьте запрос '
            f'с именем пользователя {user.username} и '
            f'кодом подтверждения {user.confirmation_code} '
            'на эндпойнт /api/v1/auth/token/.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


def username_validation(value):
    """
    Нельзя использовать имя пользователя me.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя')
    checked_value = re.match('^[\\w.@+-]+', value)
    if checked_value is None or checked_value.group() != value:
        forbidden_simbol = value[0] if (checked_value is None) \
            else value[checked_value.span()[1]]
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @ . + - _.')
    return value
