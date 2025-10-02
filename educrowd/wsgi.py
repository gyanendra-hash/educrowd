"""
WSGI config for EduCrowd project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educrowd.settings')

application = get_wsgi_application()
