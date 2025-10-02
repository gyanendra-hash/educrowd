"""
URL configuration for LMS app.
"""
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def lms_home(request):
    """
    LMS home endpoint.
    """
    return Response({
        'message': 'LMS module - Coming in Week 2',
        'features': [
            'Course Management',
            'Lesson Management',
            'Quiz & Assessment',
            'Progress Tracking',
            'Student Management',
            'Teacher Dashboard'
        ]
    })


urlpatterns = [
    path('', lms_home, name='lms-home'),
]
