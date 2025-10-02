"""
URL configuration for crowdfunding app.
"""
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def crowdfunding_home(request):
    """
    Crowdfunding home endpoint.
    """
    return Response({
        'message': 'Crowdfunding module - Coming in Week 3',
        'features': [
            'Project Creation',
            'Campaign Management',
            'Payment Processing',
            'Rewards & Perks',
            'Analytics Dashboard',
            'Backer Management'
        ]
    })


urlpatterns = [
    path('', crowdfunding_home, name='crowdfunding-home'),
]
