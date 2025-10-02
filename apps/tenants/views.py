"""
Views for tenants app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import (
    Tenant, Domain, TenantInvitation, TenantSettings, TenantAuditLog
)
from .serializers import (
    TenantSerializer, TenantCreateSerializer, TenantUpdateSerializer,
    DomainSerializer, DomainCreateSerializer, TenantInvitationSerializer,
    TenantInvitationCreateSerializer, TenantSettingsSerializer,
    TenantAuditLogSerializer, TenantStatsSerializer
)


class TenantListView(generics.ListCreateAPIView):
    """
    List or create tenants.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.request.method == 'POST':
            return TenantCreateSerializer
        return TenantSerializer
    
    def get_queryset(self):
        """Filter tenants based on user permissions."""
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()
        
        # Get tenants where user has a role
        return Tenant.objects.filter(
            user_roles__user=user,
            user_roles__is_active=True
        ).distinct()


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tenant.
    """
    queryset = Tenant.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.request.method in ['PUT', 'PATCH']:
            return TenantUpdateSerializer
        return TenantSerializer


class DomainListView(generics.ListCreateAPIView):
    """
    List or create domains for a tenant.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.request.method == 'POST':
            return DomainCreateSerializer
        return DomainSerializer
    
    def get_queryset(self):
        """Filter domains by tenant."""
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return Domain.objects.filter(tenant_id=tenant_id)
        return Domain.objects.none()


class DomainDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a domain.
    """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated]


class TenantInvitationListView(generics.ListCreateAPIView):
    """
    List or create tenant invitations.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.request.method == 'POST':
            return TenantInvitationCreateSerializer
        return TenantInvitationSerializer
    
    def get_queryset(self):
        """Filter invitations by tenant."""
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return TenantInvitation.objects.filter(tenant_id=tenant_id)
        return TenantInvitation.objects.none()


class TenantInvitationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tenant invitation.
    """
    queryset = TenantInvitation.objects.all()
    serializer_class = TenantInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_invitation(request):
    """
    Accept a tenant invitation.
    """
    token = request.data.get('token')
    if not token:
        return Response(
            {'error': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        invitation = TenantInvitation.objects.get(token=token)
    except TenantInvitation.DoesNotExist:
        return Response(
            {'error': 'Invalid invitation token'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not invitation.is_valid:
        return Response(
            {'error': 'Invitation is expired or already accepted'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user role
    from apps.users.models import UserRole
    UserRole.objects.create(
        user=request.user,
        tenant=invitation.tenant,
        role=invitation.role,
        assigned_by=invitation.invited_by
    )
    
    # Mark invitation as accepted
    invitation.is_accepted = True
    invitation.accepted_by = request.user
    invitation.accepted_at = timezone.now()
    invitation.save()
    
    # Create audit log
    TenantAuditLog.objects.create(
        tenant=invitation.tenant,
        user=request.user,
        action='invite',
        resource_type='user_role',
        description=f'User {request.user.email} accepted invitation for role {invitation.role}',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    return Response({
        'message': 'Invitation accepted successfully',
        'tenant': TenantSerializer(invitation.tenant).data
    })


class TenantSettingsView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update tenant settings.
    """
    serializer_class = TenantSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get tenant settings."""
        tenant_id = self.request.query_params.get('tenant_id')
        if not tenant_id:
            return Response(
                {'error': 'tenant_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tenant = get_object_or_404(Tenant, id=tenant_id)
        settings, created = TenantSettings.objects.get_or_create(tenant=tenant)
        return settings


class TenantAuditLogListView(generics.ListAPIView):
    """
    List tenant audit logs.
    """
    serializer_class = TenantAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter audit logs by tenant."""
        tenant_id = self.request.query_params.get('tenant_id')
        if not tenant_id:
            return TenantAuditLog.objects.none()
        
        return TenantAuditLog.objects.filter(tenant_id=tenant_id)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def tenant_stats(request):
    """
    Get tenant statistics.
    """
    tenant_id = request.query_params.get('tenant_id')
    if not tenant_id:
        return Response(
            {'error': 'tenant_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    # Calculate statistics
    from apps.users.models import UserRole
    
    total_users = UserRole.objects.filter(tenant=tenant).count()
    active_users = UserRole.objects.filter(tenant=tenant, is_active=True).count()
    total_domains = Domain.objects.filter(tenant=tenant).count()
    total_invitations = TenantInvitation.objects.filter(tenant=tenant).count()
    pending_invitations = TenantInvitation.objects.filter(
        tenant=tenant,
        is_accepted=False,
        expires_at__gt=timezone.now()
    ).count()
    total_audit_logs = TenantAuditLog.objects.filter(tenant=tenant).count()
    
    # Get recent audit logs
    recent_audit_logs = TenantAuditLog.objects.filter(
        tenant=tenant
    ).order_by('-created_at')[:10]
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'total_domains': total_domains,
        'total_invitations': total_invitations,
        'pending_invitations': pending_invitations,
        'total_audit_logs': total_audit_logs,
        'recent_audit_logs': TenantAuditLogSerializer(recent_audit_logs, many=True).data
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_invitation_email(request):
    """
    Send invitation email.
    """
    invitation_id = request.data.get('invitation_id')
    if not invitation_id:
        return Response(
            {'error': 'invitation_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    invitation = get_object_or_404(TenantInvitation, id=invitation_id)
    
    if not invitation.is_valid:
        return Response(
            {'error': 'Invitation is expired or already accepted'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Send invitation email
    from django.core.mail import send_mail
    from django.conf import settings
    
    invitation_url = f"{settings.FRONTEND_URL}/accept-invitation/{invitation.token}/"
    
    subject = f'Invitation to join {invitation.tenant.name}'
    message = f"""
    Hi,
    
    You have been invited to join {invitation.tenant.name} as a {invitation.role}.
    
    Click the link below to accept the invitation:
    {invitation_url}
    
    This invitation expires on {invitation.expires_at.strftime('%Y-%m-%d %H:%M:%S')}.
    
    If you didn't expect this invitation, please ignore this email.
    
    Best regards,
    {invitation.tenant.name} Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [invitation.email],
        fail_silently=False,
    )
    
    return Response({'message': 'Invitation email sent successfully'})
