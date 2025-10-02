"""
Django management command to create test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tenants.models import Tenant, Domain, TenantSettings
from apps.users.models import UserProfile, UserRole

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing test data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing test data...')
            User.objects.filter(username__startswith='test').delete()
            Tenant.objects.filter(name__startswith='Test').delete()

        self.stdout.write('Creating test data...')

        # Create test superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@educrowd.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(f'Created superuser: {admin_user.email}')

        # Create test regular user
        if not User.objects.filter(username='testuser').exists():
            test_user = User.objects.create_user(
                username='testuser',
                email='test@educrowd.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )
            self.stdout.write(f'Created test user: {test_user.email}')

        # Create test tenant
        if not Tenant.objects.filter(name='Test University').exists():
            tenant = Tenant.objects.create(
                name='Test University',
                description='A test educational institution',
                email='contact@testuniversity.edu',
                website='https://testuniversity.edu',
                timezone='America/New_York',
                language='en',
                currency='USD',
                created_by=User.objects.get(username='admin')
            )
            
            # Create domain for tenant
            Domain.objects.create(
                tenant=tenant,
                domain='testuniversity.localhost',
                is_primary=True
            )
            
            # Create tenant settings
            TenantSettings.objects.create(tenant=tenant)
            
            self.stdout.write(f'Created test tenant: {tenant.name}')

        # Create user roles
        admin_user = User.objects.get(username='admin')
        test_user = User.objects.get(username='testuser')
        tenant = Tenant.objects.get(name='Test University')

        # Admin role
        if not UserRole.objects.filter(user=admin_user, tenant=tenant).exists():
            UserRole.objects.create(
                user=admin_user,
                tenant=tenant,
                role='super_admin',
                assigned_by=admin_user
            )
            self.stdout.write(f'Created admin role for {admin_user.email}')

        # Test user role
        if not UserRole.objects.filter(user=test_user, tenant=tenant).exists():
            UserRole.objects.create(
                user=test_user,
                tenant=tenant,
                role='student',
                assigned_by=admin_user
            )
            self.stdout.write(f'Created student role for {test_user.email}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created test data!')
        )
        self.stdout.write('\nTest credentials:')
        self.stdout.write('Admin: admin@educrowd.com / admin123')
        self.stdout.write('User: test@educrowd.com / test123')
        self.stdout.write('\nAccess the application at: http://localhost:8000')
