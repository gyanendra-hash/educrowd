#!/usr/bin/env python
"""
EduCrowd Setup Verification Script
=================================

This script verifies that the EduCrowd Django setup is working correctly.
Run this after setting up the project to ensure everything is configured properly.

Usage:
    python test_setup.py

Requirements:
    - Python 3.8+
    - Django 4.2+
    - All dependencies installed
"""
import os
import sys
import django
from pathlib import Path
import subprocess
import time

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educrowd.settings')

# Setup Django
try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

def test_imports():
    """Test that all modules can be imported."""
    try:
        # Test core Django imports
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Test app imports
        from apps.users.models import User, UserProfile, UserRole, UserSession
        from apps.tenants.models import Tenant, Domain, TenantInvitation, TenantSettings, TenantAuditLog
        from apps.core.urls import health_check
        from apps.lms.urls import lms_home
        from apps.crowdfunding.urls import crowdfunding_home
        
        # Test serializers
        from apps.users.serializers import UserSerializer, UserCreateSerializer
        from apps.tenants.serializers import TenantSerializer, TenantCreateSerializer
        
        # Test views
        from apps.users.views import UserCreateView, LoginView
        from apps.tenants.views import TenantListView, TenantCreateView
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test that models can be created."""
    try:
        from apps.users.models import User
        from apps.tenants.models import Tenant
        
        # Test User model
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        print("✅ User model creation successful")
        
        # Test Tenant model
        tenant = Tenant(
            name='Test Tenant',
            description='Test tenant description'
        )
        print("✅ Tenant model creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Model creation error: {e}")
        return False

def test_settings():
    """Test Django settings."""
    try:
        from django.conf import settings
        
        # Check required settings
        assert hasattr(settings, 'SECRET_KEY'), "SECRET_KEY not found"
        assert hasattr(settings, 'DATABASES'), "DATABASES not found"
        assert hasattr(settings, 'INSTALLED_APPS'), "INSTALLED_APPS not found"
        assert 'apps.users' in settings.INSTALLED_APPS, "users app not in INSTALLED_APPS"
        assert 'apps.tenants' in settings.INSTALLED_APPS, "tenants app not in INSTALLED_APPS"
        assert 'apps.lms' in settings.INSTALLED_APPS, "lms app not in INSTALLED_APPS"
        assert 'apps.crowdfunding' in settings.INSTALLED_APPS, "crowdfunding app not in INSTALLED_APPS"
        assert 'apps.core' in settings.INSTALLED_APPS, "core app not in INSTALLED_APPS"
        
        # Check custom user model
        assert settings.AUTH_USER_MODEL == 'users.User', "Custom user model not configured"
        
        # Check multi-tenancy settings
        assert hasattr(settings, 'TENANT_MODEL'), "TENANT_MODEL not configured"
        assert hasattr(settings, 'TENANT_DOMAIN_MODEL'), "TENANT_DOMAIN_MODEL not configured"
        
        print("✅ Django settings validation successful")
        return True
    except Exception as e:
        print(f"❌ Settings validation error: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Test database connection
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("Please ensure PostgreSQL is running and configured correctly")
        return False

def test_redis_connection():
    """Test Redis connection."""
    try:
        from django.core.cache import cache
        
        # Test Redis connection
        cache.set('test_key', 'test_value', 10)
        result = cache.get('test_key')
        assert result == 'test_value', "Redis test failed"
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        print("Please ensure Redis is running and configured correctly")
        return False

def test_environment_file():
    """Test environment file configuration."""
    try:
        env_file = Path('.env')
        if not env_file.exists():
            print("⚠️  .env file not found. Please copy .env.example to .env")
            return False
        
        # Check if .env.example exists
        env_example = Path('.env.example')
        if not env_example.exists():
            print("❌ .env.example file not found")
            return False
        
        print("✅ Environment files found")
        return True
    except Exception as e:
        print(f"❌ Environment file error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 EduCrowd Setup Verification")
    print("=" * 50)
    print("This script will verify that your EduCrowd setup is working correctly.")
    print("=" * 50)
    
    tests = [
        ("Environment Files", test_environment_file),
        ("Import Test", test_imports),
        ("Settings Test", test_settings),
        ("Model Test", test_models),
        ("Database Connection", test_database_connection),
        ("Redis Connection", test_redis_connection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! Your EduCrowd setup is working correctly.")
        print("\n🚀 Next steps:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Start with Docker: docker-compose up --build")
        print("3. Or run locally: python run_dev.py")
        print("4. Access: http://localhost:8000")
        print("5. Admin: http://localhost:8000/admin")
        print("\n📚 Documentation:")
        print("- README.md: Project overview and setup")
        print("- ARCHITECTURE.md: Technical architecture details")
        print("- API_DOCUMENTATION.md: Complete API reference")
        print("- DEPLOYMENT.md: Production deployment guide")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that PostgreSQL and Redis are running")
        print("3. Verify your .env file configuration")
        print("4. Check the logs for detailed error messages")
        sys.exit(1)

if __name__ == '__main__':
    main()
