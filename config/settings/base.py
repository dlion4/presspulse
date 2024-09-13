# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

import os
import sys
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

from .utils import get_database_config

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# presspulse/
APPS_DIR = BASE_DIR / "presspulse"
sys.path.append(str(BASE_DIR / "website"))
env = environ.Env()

if READ_DOT_ENV_FILE := env.bool("DJANGO_READ_DOT_ENV_FILE", default=True):
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages


LANGUAGES = [
    ("en", _("English")),
    ("fr-fr", _("French")),
    ("pt-br", _("Portuguese")),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL"),
# The above code snippet is configuring database settings in a Django project. It defines two database
# configurations: "default" and "finance".
    # "finance": env.db("FINANCE_DATABASE_URL"),
    # "medical": env.db("MEDICAL_DATABASE_URL"),
    }
DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# # DATABASES["finance"]["ENGINE"] = "django_tenants.postgresql_backend"
# DATABASES["finance"]["ATOMIC_REQUESTS"] = True
# # DATABASES["medical"]["ENGINE"] = "django_tenants.postgresql_backend"
# DATABASES["medical"]["ATOMIC_REQUESTS"] = True
# WILL RUN OR CREATE MULTIPLE DATABASES WITH EACH WEBSITE HAVING ITS OWN DATABASE
DATABASE_ROUTERS = (
    "django_tenants.routers.TenantSyncRouter",
)
# Function to dynamically add a tenant database to DATABASES
def add_tenant_database(tenant_schema_name):
    DATABASES[tenant_schema_name] = {
        "ENGINE": get_database_config(tenant_schema_name)["ENGINE"],
        "NAME": tenant_schema_name,  # The dynamically created tenant database name
        "USER": get_database_config(tenant_schema_name)["USER"],
        "PASSWORD": get_database_config(tenant_schema_name)["PASSWORD"],
        "HOST": get_database_config(tenant_schema_name)["HOST"],
        "PORT": get_database_config(tenant_schema_name)["PORT"],
        "ATOMIC_REQUESTS": True,
        "TIME_ZONE": TIME_ZONE,  # Add this line
        "CONN_MAX_AGE": 0,  # Add this line if not present
        "CONN_HEALTH_CHECKS": env.bool("CONN_HEALTH_CHECKS", False),
        "OPTIONS": {},
        "TEST": {},
        "CHARSET": env.str("CHARSET", "utf8"),
        "COLLATION": env.str("COLLATION", "utf8_general_ci"),
        "AUTOCOMMIT": True,  # Explicitly set AUTOCOMMIT to True

    }

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"


MAIN_WEBSITE_APPLICATIONS = [
    "website.main.news",
    "website.main.posts",
]


# APPS
# ------------------------------------------------------------------------------
SHARED_APPS = [
    "django_tenants",  # mandatory
    # for the core hosting the domain and the clients
    "website.main.main_app",
    "website.main.news",
    "website.main.posts",

    "django_cotton.apps.SimpleAppConfig",
    # other shared django applications
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",

]


TENANT_APPS  = [
    # these are tenants applications applications
    "presspulse.users",
    # Your stuff: custom apps go here
    # MAIN APPLICATION
    # *MAIN_WEBSITE_APPLICATIONS
]


# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = SHARED_APPS + THIRD_PARTY_APPS + TENANT_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "presspulse.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
# AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    #Add the middleware django_tenants.middleware.main.TenantMainMiddleware to the top of MIDDLEWARE, so that each request can be set to use the correct schema.
    "django_tenants.middleware.main.TenantMainMiddleware",
    # custom tenant middleware for the databases
    # "website.main.main_app.middleware.TenantConnectionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://django-tenants.readthedocs.io/en/latest/files.html#specifying-a-different-target-directory
# ------------------------------------------------------------------------------
MULTITENANT_RELATIVE_STATIC_ROOT = str(BASE_DIR / "tenants/%s")

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://django-tenants.readthedocs.io/en/latest/files.html#configuring-the-static-file-finders
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",  # Must be first
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
# MULTI TENANT SETUP
# ----------------------------------------------------------------------------
MULTITENANT_STATICFILES_DIRS = [str(BASE_DIR / "tenants/%s/static")]
# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
# https://django-tenants.readthedocs.io/en/latest/files.html#specifying-a-different-target-directory
# ---------------------------------------------------------------------------
MULTITENANT_RELATIVE_MEDIA_ROOT = "%s/media_dir"

# https://django-tenants.readthedocs.io/en/latest/files.html#configuring-media-file-storage
# ---------------------------------------------------------------------------
# DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"
MULTITENANT_RELATIVE_MEDIA_ROOT = ""  # (default: create sub-directory for each tenant)
# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates


TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": False,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request", # necessary for the tenants
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django_cotton.cotton_loader.Loader",
                "django_tenants.template.loaders.filesystem.Loader",  # Must be first
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "builtins": [
                "django_cotton.templatetags.cotton",
            ],
        },
    },
]

#  https://django-tenants.readthedocs.io/en/latest/files.html#configuring-the-template-loaders
# ---------------------------------------------------------------------------------------
MULTITENANT_TEMPLATE_DIRS = [
    str(BASE_DIR / "tenants/%s/templates"),
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"
# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""jeckonia""", "jeckonia@localhost")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "presspulse API",
    "DESCRIPTION": "Documentation of API endpoints of presspulse",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SCHEMA_PATH_PREFIX": "/api/",
}
# Your stuff...
# ------------------------------------------------------------------------------
# TENANT SPECIFIC CONFIGURATIONS
# ---------------------------------------------------
TENANT_MODEL = "main_app.Client"
TENANT_DOMAIN_MODEL = "main_app.Domain"
PUBLIC_SCHEMA_URLCONF  = "website.main.urls"


