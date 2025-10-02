"""
Admin configuration for tenants app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Tenant, Domain, TenantInvitation, TenantSettings, TenantAuditLog
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """
    Tenant admin.
    """
    list_display = (
        'name', 'is_active', 'subscription_plan', 'subscription_status',
        'created_by', 'created_at', 'user_count'
    )
    list_filter = (
        'is_active', 'subscription_plan', 'subscription_status',
        'created_at', 'timezone', 'language'
    )
    search_fields = ('name', 'description', 'email', 'website')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created_at', 'updated_at', 'user_count')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'website', 'address')
        }),
        (_('Localization'), {
            'fields': ('timezone', 'language', 'currency')
        }),
        (_('Branding'), {
            'fields': ('logo',)
        }),
        (_('Subscription'), {
            'fields': (
                'subscription_plan', 'subscription_status',
                'subscription_expires_at'
            )
        }),
        (_('Configuration'), {
            'fields': ('settings', 'features'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """
    Domain admin.
    """
    list_display = (
        'domain', 'tenant', 'is_primary', 'is_ssl_enabled', 'created_at'
    )
    list_filter = ('is_primary', 'is_ssl_enabled', 'created_at')
    search_fields = ('domain', 'tenant__name')
    raw_id_fields = ('tenant',)
    readonly_fields = ('created_at',)


@admin.register(TenantInvitation)
class TenantInvitationAdmin(admin.ModelAdmin):
    """
    Tenant Invitation admin.
    """
    list_display = (
        'email', 'tenant', 'role', 'invited_by', 'is_accepted',
        'expires_at', 'created_at'
    )
    list_filter = (
        'role', 'is_accepted', 'expires_at', 'created_at'
    )
    search_fields = ('email', 'tenant__name', 'invited_by__email')
    raw_id_fields = ('tenant', 'invited_by', 'accepted_by')
    readonly_fields = ('token', 'created_at', 'accepted_at')
    
    fieldsets = (
        (None, {
            'fields': ('tenant', 'email', 'role', 'invited_by')
        }),
        (_('Status'), {
            'fields': ('is_accepted', 'accepted_by', 'accepted_at')
        }),
        (_('Security'), {
            'fields': ('token', 'expires_at')
        }),
        (_('Metadata'), {
            'fields': ('created_at',)
        }),
    )


@admin.register(TenantSettings)
class TenantSettingsAdmin(admin.ModelAdmin):
    """
    Tenant Settings admin.
    """
    list_display = (
        'tenant', 'enable_lms', 'enable_crowdfunding',
        'enable_analytics', 'created_at'
    )
    list_filter = (
        'enable_lms', 'enable_crowdfunding', 'enable_analytics',
        'enable_notifications', 'created_at'
    )
    search_fields = ('tenant__name',)
    raw_id_fields = ('tenant',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Branding'), {
            'fields': (
                'primary_color', 'secondary_color',
                'logo_url', 'favicon_url'
            )
        }),
        (_('Features'), {
            'fields': (
                'enable_lms', 'enable_crowdfunding',
                'enable_analytics', 'enable_notifications'
            )
        }),
        (_('Security'), {
            'fields': (
                'password_min_length', 'password_require_special',
                'session_timeout', 'max_login_attempts'
            )
        }),
        (_('Notifications'), {
            'fields': (
                'email_notifications', 'sms_notifications',
                'push_notifications'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TenantAuditLog)
class TenantAuditLogAdmin(admin.ModelAdmin):
    """
    Tenant Audit Log admin.
    """
    list_display = (
        'tenant', 'user', 'action', 'resource_type',
        'ip_address', 'created_at'
    )
    list_filter = (
        'action', 'resource_type', 'created_at'
    )
    search_fields = (
        'tenant__name', 'user__email', 'description',
        'resource_type', 'resource_id'
    )
    raw_id_fields = ('tenant', 'user')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('tenant', 'user', 'action', 'resource_type', 'resource_id')
        }),
        (_('Details'), {
            'fields': ('description', 'metadata')
        }),
        (_('Request Info'), {
            'fields': ('ip_address', 'user_agent')
        }),
        (_('Metadata'), {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding audit logs manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing audit logs."""
        return False
