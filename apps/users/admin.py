"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserRole, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin.
    """
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_staff', 'is_verified', 'is_active', 'created_at'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'is_verified',
        'created_at', 'last_login'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number',
                'avatar', 'date_of_birth', 'bio'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile admin.
    """
    list_display = (
        'user', 'organization', 'job_title', 'location',
        'timezone', 'language', 'created_at'
    )
    list_filter = ('timezone', 'language', 'created_at')
    search_fields = (
        'user__email', 'user__username', 'organization',
        'job_title', 'location'
    )
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    User Role admin.
    """
    list_display = (
        'user', 'tenant', 'role', 'is_active',
        'assigned_by', 'assigned_at', 'expires_at'
    )
    list_filter = (
        'role', 'is_active', 'assigned_at', 'expires_at'
    )
    search_fields = (
        'user__email', 'user__username', 'tenant__name'
    )
    raw_id_fields = ('user', 'tenant', 'assigned_by')
    readonly_fields = ('assigned_at',)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    User Session admin.
    """
    list_display = (
        'user', 'session_key', 'ip_address',
        'is_active', 'last_activity', 'created_at'
    )
    list_filter = ('is_active', 'created_at', 'last_activity')
    search_fields = ('user__email', 'user__username', 'session_key', 'ip_address')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'last_activity')
