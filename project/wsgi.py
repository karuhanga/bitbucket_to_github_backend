"""
WSGI config for bitbucket_github_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from project.settings.utils import load_settings

load_settings()

application = get_wsgi_application()
