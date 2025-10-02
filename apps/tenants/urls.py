"""
URL configuration for tenants app.
"""
from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    # Tenant management
    path('', views.TenantListView.as_view(), name='tenant-list'),
    path('<int:pk>/', views.TenantDetailView.as_view(), name='tenant-detail'),
    path('stats/', views.tenant_stats, name='tenant-stats'),
    
    # Domain management
    path('domains/', views.DomainListView.as_view(), name='domain-list'),
    path('domains/<int:pk>/', views.DomainDetailView.as_view(), name='domain-detail'),
    
    # Invitation management
    path('invitations/', views.TenantInvitationListView.as_view(), name='invitation-list'),
    path('invitations/<int:pk>/', views.TenantInvitationDetailView.as_view(), name='invitation-detail'),
    path('invitations/accept/', views.accept_invitation, name='accept-invitation'),
    path('invitations/send-email/', views.send_invitation_email, name='send-invitation-email'),
    
    # Settings
    path('settings/', views.TenantSettingsView.as_view(), name='tenant-settings'),
    
    # Audit logs
    path('audit-logs/', views.TenantAuditLogListView.as_view(), name='audit-log-list'),
]
