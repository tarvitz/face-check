"""
Django settings for face_check project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from datetime import datetime
from . utils import get_env_string, get_env_bool, get_env_int, rel

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_string(
    'SECRET_KEY', '1z9h6)&==7w@-cm-we#4ky3m-ar8g&+(jpozx0kxubs7b1s2m*'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_bool('DEBUG', False)

ALLOWED_HOSTS = get_env_string('ALLOWED_HOSTS', '').split(',')
AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitch.TwitchOAuth2',
    'face_check.social.backends.goodgame.GoodGameOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Application definition

INSTALLED_APPS = [
    #: system apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #: internal apps
    'face_check.health.apps.HealthApp',
    'face_check.accounts.apps.AccountsConfig',

    #: third parties
    'social_django.config.PythonSocialAuthConfig',
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

ROOT_URLCONF = 'face_check.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            rel('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #: third parties
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

                #: applications
                'face_check.accounts.context_processors.secret'
            ],
        },
    },
]

WSGI_APPLICATION = 'face_check.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_env_string('DATABASE_ENGINE',
                                 'django.db.backends.sqlite3'),
        'NAME': get_env_string('DATABASE_NAME', rel('db.sqlite3')),
        'USER': get_env_string('DATABASE_USER', ''),
        'PASSWORD': get_env_string('DATABASE_PASSWORD', ''),
        'HOST': get_env_string('DATABASE_HOST', ''),
        'PORT': get_env_int('DATABASE_PORT', 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

#: AUTHENTICATIONS
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = get_env_string('STATIC_ROOT', rel('static'))

#: Third party settings

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    #: email association is disabled by default, in case of issues
    #: it's safe to disable it and use single account per social network
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    #: order is prior, twitch could be used after create_user,
    #: gg requires social auth token
    #: note that verification could be a little bit sub-optimal ;)
    'face_check.social.injector.verify',  #: user bound modification
)

#: Application settings

#: followers should be subscribed to channel not earlier than offset
FACE_CHECK_DATE_OFFSET = datetime.fromtimestamp(
    #: 2019-01-01
    float(get_env_string('FACE_CHECK_DATE_OFFSET', '1546290000.0'))
)

#: twitch channel (basically it's a user id) to provide a face check against
TWITCH_FACE_CHECK_CHANNEL = get_env_string(
    'TWITCH_FACE_CHECK_CHANNEL',
    '17861167'
)  #: wellplayedtv1

#: good game (player identifier, could be fetched from
#: https://goodgame.ru/api/getggchannelstatus?id=<channel_name>&fmt=json
#: where channel_name is a public channel name
GOOD_GAME_FACE_CHECK_CHANNEL = get_env_string(
    'GOOD_GAME_FACE_CHECK_CHANNEL',
    '1850'
)

#: import secrets settings
try:
    from . secrets import *  # NOQA
except ImportError:
    pass
