"""
User models for EduCrowd platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True
    )
    bio = models.TextField(
        _('bio'),
        max_length=500,
        blank=True
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether this user has verified their email.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users_user'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self):
        """Return the user's initials."""
        first_initial = self.first_name[0].upper() if self.first_name else ''
        last_initial = self.last_name[0].upper() if self.last_name else ''
        return f"{first_initial}{last_initial}"


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    organization = models.CharField(
        _('organization'),
        max_length=255,
        blank=True
    )
    job_title = models.CharField(
        _('job title'),
        max_length=255,
        blank=True
    )
    website = models.URLField(
        _('website'),
        blank=True
    )
    location = models.CharField(
        _('location'),
        max_length=255,
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
    notification_preferences = models.JSONField(
        _('notification preferences'),
        default=dict,
        blank=True
    )
    privacy_settings = models.JSONField(
        _('privacy settings'),
        default=dict,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        db_table = 'users_userprofile'

    def __str__(self):
        return f"{self.user.email} - Profile"


class UserRole(models.Model):
    """
    User roles within tenants.
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('contributor', 'Contributor'),
        ('viewer', 'Viewer'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=ROLE_CHOICES
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_roles'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        _('expires at'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')
        db_table = 'users_userrole'
        unique_together = ['user', 'tenant', 'role']

    def __str__(self):
        return f"{self.user.email} - {self.role} in {self.tenant.name}"

    @property
    def is_expired(self):
        """Check if the role has expired."""
        if not self.expires_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at


class UserSession(models.Model):
    """
    Track user sessions for security and analytics.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    session_key = models.CharField(
        _('session key'),
        max_length=40,
        unique=True
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
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    last_activity = models.DateTimeField(
        _('last activity'),
        auto_now=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('User Session')
        verbose_name_plural = _('User Sessions')
        db_table = 'users_usersession'

    def __str__(self):
        return f"{self.user.email} - {self.session_key}"

    @property
    def is_expired(self):
        """Check if the session has expired."""
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.last_activity + timedelta(hours=24)
