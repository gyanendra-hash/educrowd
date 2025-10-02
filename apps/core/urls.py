"""
URL configuration for core app.
"""
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def core_home(request):
    """
    Core home endpoint.
    """
    return Response({
        'message': 'Core module - Common utilities and shared functionality',
        'features': [
            'Health Check',
            'System Status',
            'Analytics',
            'Notifications',
            'File Management',
            'Search & Filtering'
        ]
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'message': 'EduCrowd API is running',
        'version': '1.0.0'
    })


urlpatterns = [
    path('', core_home, name='core-home'),
    path('health/', health_check, name='health-check'),
]
