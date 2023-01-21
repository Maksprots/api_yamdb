from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """Конфиг пользовательской модели в админке."""

    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    list_editable = (
        'username',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
