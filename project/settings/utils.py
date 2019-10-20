import os


def load_settings():
    environment = os.environ.get('ENVIRONMENT', 'production')
    if environment == 'development':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "project.settings.development")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "project.settings.production")
