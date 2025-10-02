"""
Tenant models for multi-tenancy support.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Tenant(TenantMixin):
    """
    Tenant model for multi-tenancy.
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='tenant_logos/',
        blank=True,
        null=True
    )
    website = models.URLField(
        _('website'),
        blank=True
    )
    email = models.EmailField(
        _('email'),
        blank=True
    )
    phone = models.CharField(
        _('phone'),
        max_length=20,
        blank=True
    )
    address = models.TextField(
        _('address'),
        blank=True
    )
    timezone = models.CharField(
        _('timezone'),
        max_length=50,
        default='UTC'
    )
    language = models.CharField(
        _('language'),
        max_length=10,
        default='en'
    )
    currency = models.CharField(
        _('currency'),
        max_length=3,
        default='USD'
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tenants'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Tenant-specific settings
    settings = models.JSONField(
        _('settings'),
        default=dict,
        blank=True,
        help_text=_('Tenant-specific configuration settings')
    )
    
    # Feature flags
    features = models.JSONField(
        _('features'),
        default=dict,
        blank=True,
        help_text=_('Enabled features for this tenant')
    )
    
    # Subscription information
    subscription_plan = models.CharField(
        _('subscription plan'),
        max_length=50,
        default='free'
    )
    subscription_status = models.CharField(
        _('subscription status'),
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended'),
            ('cancelled', 'Cancelled'),
        ],
        default='active'
    )
    subscription_expires_at = models.DateTimeField(
        _('subscription expires at'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')
        db_table = 'tenants_tenant'

    def __str__(self):
        return self.name

    @property
    def is_subscription_active(self):
        """Check if subscription is active."""
        if self.subscription_status != 'active':
            return False
        if self.subscription_expires_at:
            from django.utils import timezone
            return timezone.now() < self.subscription_expires_at
        return True

    @property
    def user_count(self):
        """Get number of users in this tenant."""
        return self.user_roles.filter(is_active=True).count()

    def get_feature(self, feature_name, default=False):
        """Get feature flag value."""
        return self.features.get(feature_name, default)

    def set_feature(self, feature_name, value):
        """Set feature flag value."""
        if not self.features:
            self.features = {}
        self.features[feature_name] = value
        self.save(update_fields=['features'])


class Domain(DomainMixin):
    """
    Domain model for tenant domains.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='domains'
    )
    is_primary = models.BooleanField(
        _('primary'),
        default=False,
        help_text=_('Primary domain for this tenant')
    )
    is_ssl_enabled = models.BooleanField(
        _('SSL enabled'),
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')
        db_table = 'tenants_domain'

    def __str__(self):
        return f"{self.domain} ({self.tenant.name})"

    def save(self, *args, **kwargs):
        """Ensure only one primary domain per tenant."""
        if self.is_primary:
            # Remove primary flag from other domains of this tenant
            Domain.objects.filter(
                tenant=self.tenant,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class TenantInvitation(models.Model):
    """
    Tenant invitation model.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    email = models.EmailField(_('email'))
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('teacher', 'Teacher'),
            ('student', 'Student'),
            ('contributor', 'Contributor'),
            ('viewer', 'Viewer'),
        ]
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invitations'
    )
    token = models.CharField(
        _('token'),
        max_length=100,
        unique=True
    )
    is_accepted = models.BooleanField(
        _('accepted'),
        default=False
    )
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_invitations'
    )
    expires_at = models.DateTimeField(_('expires at'))
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(
        _('accepted at'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Tenant Invitation')
        verbose_name_plural = _('Tenant Invitations')
        db_table = 'tenants_tenantinvitation'
        unique_together = ['tenant', 'email']

    def __str__(self):
        return f"{self.email} - {self.tenant.name} ({self.role})"

    @property
    def is_expired(self):
        """Check if invitation has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """Check if invitation is valid."""
        return not self.is_accepted and not self.is_expired


class TenantSettings(models.Model):
    """
    Tenant-specific settings model.
    """
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='tenant_settings'
    )
    
    # Branding settings
    primary_color = models.CharField(
        _('primary color'),
        max_length=7,
        default='#007bff'
    )
    secondary_color = models.CharField(
        _('secondary color'),
        max_length=7,
        default='#6c757d'
    )
    logo_url = models.URLField(
        _('logo URL'),
        blank=True
    )
    favicon_url = models.URLField(
        _('favicon URL'),
        blank=True
    )
    
    # Feature settings
    enable_lms = models.BooleanField(
        _('enable LMS'),
        default=True
    )
    enable_crowdfunding = models.BooleanField(
        _('enable crowdfunding'),
        default=True
    )
    enable_analytics = models.BooleanField(
        _('enable analytics'),
        default=True
    )
    enable_notifications = models.BooleanField(
        _('enable notifications'),
        default=True
    )
    
    # Security settings
    password_min_length = models.PositiveIntegerField(
        _('password min length'),
        default=8
    )
    password_require_special = models.BooleanField(
        _('password require special'),
        default=True
    )
    session_timeout = models.PositiveIntegerField(
        _('session timeout (minutes)'),
        default=480
    )
    max_login_attempts = models.PositiveIntegerField(
        _('max login attempts'),
        default=5
    )
    
    # Notification settings
    email_notifications = models.BooleanField(
        _('email notifications'),
        default=True
    )
    sms_notifications = models.BooleanField(
        _('SMS notifications'),
        default=False
    )
    push_notifications = models.BooleanField(
        _('push notifications'),
        default=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Tenant Settings')
        verbose_name_plural = _('Tenant Settings')
        db_table = 'tenants_tenantsettings'

    def __str__(self):
        return f"{self.tenant.name} - Settings"


class TenantAuditLog(models.Model):
    """
    Tenant audit log for tracking actions.
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('invite', 'Invite'),
        ('remove', 'Remove'),
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(
        _('action'),
        max_length=20,
        choices=ACTION_CHOICES
    )
    resource_type = models.CharField(
        _('resource type'),
        max_length=50
    )
    resource_id = models.CharField(
        _('resource ID'),
        max_length=100,
        blank=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    metadata = models.JSONField(
        _('metadata'),
        default=dict,
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP address'),
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        _('user agent'),
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Tenant Audit Log')
        verbose_name_plural = _('Tenant Audit Logs')
        db_table = 'tenants_tenantauditlog'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant.name} - {self.action} - {self.resource_type}"
