"""
Django settings for ultimate_frisbee_management project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*sg+%tkn(-7cn=k$^2!zk-z5i65f4y4cu+2v!@mw)xq$rb=u4="


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}

ALLOWED_HOSTS = [
    "venv.hbqg3zr3a3.us-west-2.elasticbeanstalk.com",
    "localhost",
    "127.0.0.1",
    "django",
    "62.178.108.138",
    "frisbee-db.flokain.com",
    "frisbee-db-test.oefsv.at",
    "159.69.181.225",
]

# Application definition

INSTALLED_APPS = [
    "ultimate_frisbee_management",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    #'silk',
    #'debug_toolbar',
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "viewflow",
    "guardian",
    "imagekit",
    "dbbackup",
    "django_crontab",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
    "sesame.backends.ModelBackend",
)

MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "sesame.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = "ultimate_frisbee_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "ultimate_frisbee_management.jinja2.environment"},
    },
]


WSGI_APPLICATION = "ultimate_frisbee_management.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #  {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    #  {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    #  {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Vienna"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/static_data"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/media"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ],
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "ultimate_frisbee_management.serializers.CustomUserDetailsSerializer",
}
LOGIN_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

ACCOUNT_LOGOUT_ON_GET = True
FAKER_LOCALE = None  # settings.LANGUAGE_CODE is loaded
FAKER_PROVIDERS = None  # faker.DEFAULT_PROVIDERS is loaded (all)

GUARDIAN_RENDER_403 = True

SESAME_MAX_AGE = 14 * 24 * 60 * 60  # Magic link tokens last 14 days
SESAME_ONE_TIME = True

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/workspace/backend/backups/"}
DBBACKUP_GPG_RECIPIENT = "CB82E38C91C67116"

CRONJOBS = [("0 3 * * *", "ultimate_frisbee_management.cron.backup")]
# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.w0103e8b.kasserver.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "admin<datenbank@frisbeeverband.at>"
