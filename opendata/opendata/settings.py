#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for opendata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from django.conf.global_settings import TEMPLATE_LOADERS as TL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Must be defined in localsettings.py
# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'lk4z2gha-+xme92dj^u$g_8&za(%ho(5!7$+63z6^0!j0ke6+s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
USE_DJANGO_EXTENSIONS = False
USE_DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]


# Application definition

# The module which list the resources to include in the application
import resources.resources.all_resources as opendata_resources
RESOURCES_MODULE_LIST = opendata_resources

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'foundation',

    'opendata',
    'resources',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'resources.context_processors.get_resources',
)

TEMPLATE_LOADERS = (
    'resources.loaders.Loader',
) + TL

ROOT_URLCONF = 'opendata.urls'

WSGI_APPLICATION = 'opendata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# The absolute path to the directory where collectstatic will collect static
# files for deployment.
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static') + os.path.sep
# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

###############################################################################
# LOCAL SETTINGS
###############################################################################

# Import local settings
try:
    from .localsettings import *
except ImportError:
    pass

if USE_DJANGO_EXTENSIONS:
    INSTALLED_APPS += ('django_extensions', )

if USE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar', )
