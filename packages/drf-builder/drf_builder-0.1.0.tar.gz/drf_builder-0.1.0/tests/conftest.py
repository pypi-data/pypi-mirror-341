"""
Configuração para os testes do drf-builder.
"""
import os
import django
from django.conf import settings

# Configure settings mínimas para os testes
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'rest_framework',
            'tests',
        ],
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'drf_builder.middleware.APIExceptionMiddleware',
        ],
        SECRET_KEY='dummy-key-for-tests',
        USE_TZ=True,
        TIME_ZONE='UTC',
    )

    django.setup()