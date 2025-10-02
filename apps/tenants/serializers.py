"""
Serializers for tenants app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Tenant, Domain, TenantInvitation, TenantSettings, TenantAuditLog
)

User = get_user_model()


class TenantSerializer(serializers.ModelSerializer):
    """
    Tenant serializer.
    """
    user_count = serializers.ReadOnlyField()
    is_subscription_active = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'description', 'logo', 'website', 'email',
            'phone', 'address', 'timezone', 'language', 'currency',
            'is_active', 'created_by', 'created_by_name', 'created_at',
            'updated_at', 'settings', 'features', 'subscription_plan',
            'subscription_status', 'subscription_expires_at',
            'user_count', 'is_subscription_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_count']


class TenantCreateSerializer(serializers.ModelSerializer):
    """
    Tenant creation serializer.
    """
    domain = serializers.CharField(write_only=True, help_text="Primary domain for the tenant")
    
    class Meta:
        model = Tenant
        fields = [
            'name', 'description', 'logo', 'website', 'email',
            'phone', 'address', 'timezone', 'language', 'currency',
            'settings', 'features', 'domain'
        ]
    
    def create(self, validated_data):
        """Create tenant with domain."""
        domain = validated_data.pop('domain')
        tenant = Tenant.objects.create(**validated_data)
        
        # Create primary domain
        Domain.objects.create(
            tenant=tenant,
            domain=domain,
            is_primary=True
        )
        
        # Create default settings
        TenantSettings.objects.create(tenant=tenant)
        
        return tenant


class TenantUpdateSerializer(serializers.ModelSerializer):
    """
    Tenant update serializer.
    """
    class Meta:
        model = Tenant
        fields = [
            'name', 'description', 'logo', 'website', 'email',
            'phone', 'address', 'timezone', 'language', 'currency',
            'is_active', 'settings', 'features', 'subscription_plan',
            'subscription_status', 'subscription_expires_at'
        ]


class DomainSerializer(serializers.ModelSerializer):
    """
    Domain serializer.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = Domain
        fields = [
            'id', 'domain', 'tenant', 'tenant_name', 'is_primary',
            'is_ssl_enabled', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DomainCreateSerializer(serializers.ModelSerializer):
    """
    Domain creation serializer.
    """
    class Meta:
        model = Domain
        fields = ['domain', 'tenant', 'is_primary', 'is_ssl_enabled']


class TenantInvitationSerializer(serializers.ModelSerializer):
    """
    Tenant Invitation serializer.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    invited_by_name = serializers.CharField(source='invited_by.full_name', read_only=True)
    accepted_by_name = serializers.CharField(source='accepted_by.full_name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = TenantInvitation
        fields = [
            'id', 'tenant', 'tenant_name', 'email', 'role',
            'invited_by', 'invited_by_name', 'token', 'is_accepted',
            'accepted_by', 'accepted_by_name', 'expires_at',
            'created_at', 'accepted_at', 'is_expired', 'is_valid'
        ]
        read_only_fields = ['id', 'token', 'created_at', 'accepted_at']


class TenantInvitationCreateSerializer(serializers.ModelSerializer):
    """
    Tenant Invitation creation serializer.
    """
    class Meta:
        model = TenantInvitation
        fields = ['tenant', 'email', 'role', 'expires_at']
    
    def create(self, validated_data):
        """Create invitation with token."""
        import secrets
        import string
        from django.utils import timezone
        from datetime import timedelta
        
        # Generate secure token
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(50))
        
        # Set default expiration (7 days from now)
        if not validated_data.get('expires_at'):
            validated_data['expires_at'] = timezone.now() + timedelta(days=7)
        
        invitation = TenantInvitation.objects.create(
            token=token,
            invited_by=self.context['request'].user,
            **validated_data
        )
        
        return invitation


class TenantSettingsSerializer(serializers.ModelSerializer):
    """
    Tenant Settings serializer.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = TenantSettings
        fields = [
            'id', 'tenant', 'tenant_name', 'primary_color', 'secondary_color',
            'logo_url', 'favicon_url', 'enable_lms', 'enable_crowdfunding',
            'enable_analytics', 'enable_notifications', 'password_min_length',
            'password_require_special', 'session_timeout', 'max_login_attempts',
            'email_notifications', 'sms_notifications', 'push_notifications',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TenantAuditLogSerializer(serializers.ModelSerializer):
    """
    Tenant Audit Log serializer.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = TenantAuditLog
        fields = [
            'id', 'tenant', 'tenant_name', 'user', 'user_name',
            'action', 'resource_type', 'resource_id', 'description',
            'metadata', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TenantStatsSerializer(serializers.Serializer):
    """
    Tenant statistics serializer.
    """
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_domains = serializers.IntegerField()
    total_invitations = serializers.IntegerField()
    pending_invitations = serializers.IntegerField()
    total_audit_logs = serializers.IntegerField()
    recent_audit_logs = TenantAuditLogSerializer(many=True)
