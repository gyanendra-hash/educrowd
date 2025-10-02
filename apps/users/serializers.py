"""
Serializers for users app.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, UserRole, UserSession


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    full_name = serializers.ReadOnlyField()
    initials = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'initials', 'phone_number', 'avatar',
            'date_of_birth', 'bio', 'is_verified', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    User creation serializer.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'phone_number',
            'date_of_birth', 'bio'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    User update serializer.
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'avatar', 'date_of_birth', 'bio'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile serializer.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'organization', 'job_title', 'website',
            'location', 'timezone', 'language', 'notification_preferences',
            'privacy_settings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRoleSerializer(serializers.ModelSerializer):
    """
    User Role serializer.
    """
    user = UserSerializer(read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.full_name', read_only=True)
    
    class Meta:
        model = UserRole
        fields = [
            'id', 'user', 'tenant', 'tenant_name', 'role',
            'is_active', 'assigned_by', 'assigned_by_name',
            'assigned_at', 'expires_at'
        ]
        read_only_fields = ['id', 'assigned_at']


class LoginSerializer(serializers.Serializer):
    """
    Login serializer.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Validate user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    Password change serializer.
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        """Validate password change."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Password reset request serializer.
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email exists."""
        try:
            User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('No active user found with this email.')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Password reset confirmation serializer.
    """
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        """Validate password reset confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs


class UserSessionSerializer(serializers.ModelSerializer):
    """
    User Session serializer.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'session_key', 'ip_address',
            'user_agent', 'is_active', 'last_activity', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'last_activity']
