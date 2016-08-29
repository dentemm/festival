"""
Django settings for festival project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

os.environ['S3_USE_SIGV4'] = 'True'
os.environ['SWF'] = 'eu-central-1'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',


    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'compressor',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third party apps
    'django_countries',                 # automatisch invullen van landen bij adres model
    'django_comments',                  # comments toevoegen aan festivals 
    'storages',                         # wordt gebruikt om media files naar Amazon S3 te uploaden
    'social.apps.django_app.default',   # laat toe om in te loggen via social media platforms
    'geopy',                            # maakt het mogelijk om een adres te geocoderen (adres => lat + long)
    'widget_tweaks',                    # om forms te stylen
    #'recurrence',

    # Custom non-wagtail apps
    'comments',
    'ratings',
    'festivaluser',
]

# CUSTOMIZING DJANGO CONTRIB COMMENTS
COMMENTS_APP = 'comments'
COMMENT_MAX_LENGTH = 700

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'festival.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Context processor for python-social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'festival.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'festival_db',                      # Or path to database file if using sqlite3.
        #'NAME': 'test',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}   

AUTHENTICATION_BACKENDS = (
    # ondersteunde python-social-auth authentication backends
    'social.backends.facebook.FacebookOAuth2',

    # default django auth backend
    'django.contrib.auth.backends.ModelBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'nl-BE'
#LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

import locale
locale.setlocale(locale.LC_ALL, 'nl_BE.UTF-8')

# WAGTAIL SETTINGS

# Naam van website
WAGTAIL_SITE_NAME = "festival"

# Custom image model
WAGTAILIMAGES_IMAGE_MODEL = 'home.CustomImage'

# Wagtail Search settings
WAGTAILSEARCH_RESULTS_TEMPLATE = '404.html'
WAGTAILSEARCH_RESULTS_TEMPLATE_AJAX = 'home/templates/home/search/search_results.html'


# PYTHON SOCIAL AUTH settings
#SOCIAL_AUTH_USER_MODEL = 'festivaluser.models.FestivalAdvisorUser'
#SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.User'

SOCIAL_AUTH_PIPELINE = (
    # GET USER INFO
    'social.pipeline.social_auth.social_details',
    # GET USER UUID FROM AUTH BACKEND SERVICE
    'social.pipeline.social_auth.social_uid',
    # AUTH ALLOWED?
    'social.pipeline.social_auth.auth_allowed',
    # CHECK IF EXISTS
    'social.pipeline.social_auth.social_user',
    # CREATE DJANGO USERNAME
    'social.pipeline.user.get_username',
    # CREATE DJANGO USER OBJECT IF NEW
    'social.pipeline.user.create_user',
    # --- CUSTOM!!!! ---
    'festivaluser.pipeline.save_profile',  # <--- set the path to the function
    # LINK NEW DJANGO USER OBJECT WITH CURRENT AUTH USER
    'social.pipeline.social_auth.associate_user',
    # EXTRA_DATA FIELD IS INSTANTIATED WITH WHICHEVER DATA I REQUEST
    'social.pipeline.social_auth.load_extra_data',
    # UPDATE USER RECORD WITH CHANGED INFO FROM AUTH SERVIVE
    'social.pipeline.user.user_details',
)

SESSION_COOKIE_SECURE=False

