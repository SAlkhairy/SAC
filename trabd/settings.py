"""
Django settings for trabd project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import secrets
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getattr(secrets, 'DEBUG', True)

ALLOWED_HOSTS = ['127.0.0.1', '.trabdportal.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'bootstrap3',
    'voting',
    'accounts',
    'userena',
    'guardian',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trabd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'trabd.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DEFAULT_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = getattr(secrets, 'DATABASES', DEFAULT_DATABASES)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
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

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_BACKEND = getattr(secrets, 'EMAIL_BACKEND', 'django.core.mail.backends.dummy.EmailBackend')
DEFAULT_FROM_EMAIL = 'noreply@trabdportal.com'
EMAIL_USE_TLS = getattr(secrets, 'EMAIL_USE_TLS', True)
EMAIL_HOST = getattr(secrets, 'EMAIL_HOST', '')
EMAIL_PORT = getattr(secrets, 'EMAIL_PORT', 0)
EMAIL_HOST_USER = getattr(secrets, 'EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = getattr(secrets, 'EMAIL_HOST_PASSWORD', '')

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.Profile'


USERENA_SIGNIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ar-SA'

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = getattr(secrets, 'STATIC_ROOT', None)
MEDIA_URL = '/media/'

DEFAULT_MEDIA = BASE_DIR + '/media/'
MEDIA_ROOT = getattr(secrets, 'MEDIA_ROOT', DEFAULT_MEDIA)
