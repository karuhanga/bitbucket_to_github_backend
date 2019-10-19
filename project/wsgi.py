"""
WSGI config for bitbucket_github_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get('ENVIRONMENT', 'production')
if environment == 'development':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "project.settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "project.settings.production")

application = get_wsgi_application()
