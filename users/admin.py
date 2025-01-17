from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import UserRefreshToken

User = get_user_model()


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


@admin.register(UserRefreshToken)
class UserRefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'refresh_token', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
