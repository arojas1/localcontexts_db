"""
Django settings for localcontexts project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['PROD_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG_VALUE'] == 'True'

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/1.10/ref/settings/
# Also see https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/django/mysite/settings.py
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-ADMINS
# For when DEBUG = FALSE, sends emails with site errors
SITE_ADMIN_NAME = os.environ['SITE_ADMIN_NAME']
SITE_ADMIN_EMAIL = os.environ['SITE_ADMIN_EMAIL']
ADMINS = [(SITE_ADMIN_NAME, SITE_ADMIN_EMAIL)]

# reCAPTCHA 
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']

# Application definition
INSTALLED_APPS = [
    'maintenance_mode',
    'accounts.apps.AccountsConfig',
    'notifications.apps.NotificationsConfig',
    'bclabels.apps.BclabelsConfig',
    'researchers.apps.ResearchersConfig',
    'projects.apps.ProjectsConfig',
    'tklabels.apps.TklabelsConfig',

    'communities',
    'institutions',
    'api',
    'helpers',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'django_countries',
    'django_cleanup',
    'storages',

    'rest_framework',
    'corsheaders',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CONTEXT_PROCESSORS = [
    'maintenance_mode.context_processors.maintenance_mode',
]

ROOT_URLCONF = 'localcontexts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'localcontexts.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if os.getenv('GAE_APPLICATION', None):
    """Setup Google App Engine-specific options."""

    from google.oauth2 import service_account

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'HOST': '/cloudsql/' + os.environ.get('DB_HOST')
        }
    }
    GS_BUCKET_NAME = os.environ.get('GCS_BUCKET', 'anth-ja77-local-contexts-8985.appspot.com')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'django-storages-gcs-key.json')
    )
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    MAINTENANCE_MODE_STATE_BACKEND = 'localcontexts.storage_backends.GCSDefaultStorageBackend'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT')
        }
    }
# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
# if True the superuser will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_SUPERUSER = True

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Messages
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'error-msg',
    messages.SUCCESS: 'success-msg',
    messages.INFO: 'info-msg',
}

# MailGun Configs
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_BASE_URL = os.environ.get('MAILGUN_BASE_URL')

# Config for sending out emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'localcontexts/static')
]

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Session expires after an hour of inactivity.
# Note: this will UPDATE the db on every request.
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# debug_toolbar
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True