# -*- coding: utf-8 -*-
from configurations import Configuration
from django.contrib.messages import constants as messages
from kaio import Options
from kaio.mixins import (CachesMixin, DatabasesMixin, LogsMixin, PathsMixin, SecurityMixin,
                         DebugMixin, WhiteNoiseMixin)
from os.path import join
from bima_core.constants import DEFAULT_CONSTANCE, RQ_UPLOAD_QUEUE, RQ_HAYSTACK_PHOTO_INDEX_QUEUE
from bima_core.storage import file_system_storage


opts = Options()


class Base(CachesMixin, DatabasesMixin, PathsMixin, LogsMixin, SecurityMixin, DebugMixin,
           WhiteNoiseMixin, Configuration):
    """
    Project settings for development and production.
    """

    DEBUG = opts.get('DEBUG', True)

    BASE_DIR = opts.get('APP_ROOT', None)
    APP_SLUG = opts.get('APP_SLUG', 'bima-core')
    SITE_ID = 1
    SECRET_KEY = opts.get('SECRET_KEY', 'key')

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = 'en'
    LANGUAGES = [
        ('en', 'English'),
        ('es', 'Español'),
        ('ca', 'Català'),
    ]
    TIME_ZONE = 'Europe/Madrid'

    # Model translation
    MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'es', 'ca')

    ROOT_URLCONF = 'main.urls'
    WSGI_APPLICATION = 'main.wsgi.application'

    INSTALLED_APPS = [
        # important order
        'modeltranslation',

        # django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # haystack must be before models definition
        'haystack',

        # apps
        'main',

        # 3rd parties
        'constance',
        'constance.backends.database',
        'django_extensions',
        'django_rq',
        'django_yubin',
        'kaio',
        'logentry_admin',
        'import_export',

        # 3rd parties bima
        'categories',
        'storages',
        'geoposition',
        'taggit',

        # rest framework
        'drf_chunked_upload',
        'dry_rest_permissions',
        'generic_relations',
        'rest_framework',
        'rest_framework.authtoken',
        'rest_framework_swagger',
        'taggit_serializer',

        # bima core
        'bima_core',
        'bima_core.private_api',

        # 3rd parties bima that needs fixes
        'categories.editor',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

    # SecurityMiddleware options
    SECURE_BROWSER_XSS_FILTER = True

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert additional TEMPLATE_DIRS here
                # ldapdti/templates', # optional (used in password change)
            ],
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.tz",
                    'django.template.context_processors.request',
                    'constance.context_processors.config',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            },
        },
    ]

    # User model
    AUTH_USER_MODEL = 'bima_core.User'

    if not DEBUG:
        TEMPLATES[0]['OPTIONS']['loaders'] = [
            ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
        ]

    # Email
    EMAIL_BACKEND = 'django_yubin.smtp_queue.EmailBackend'
    DEFAULT_FROM_EMAIL = opts.get('DEFAULT_FROM_EMAIL', 'Example <info@example.com>')
    MAILER_LOCK_PATH = join(BASE_DIR, 'send_mail')

    # Bootstrap 3 alerts integration with Django messages
    MESSAGE_TAGS = {
        messages.ERROR: 'danger',
    }

    # Constance
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
    CONSTANCE_CONFIG = dict(DEFAULT_CONSTANCE)

    # Django Geoposition
    GEOPOSITION_GOOGLE_MAPS_API_KEY = opts.get('GEOPOSITION_GOOGLE_MAPS_API_KEY', '')

    # Django Categories
    CATEGORIES_SETTINGS = {
        'REGISTER_ADMIN': False
    }

    # AWS
    DEFAULT_FILE_STORAGE = opts.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
    AWS_STORAGE_BUCKET_NAME = opts.get('AWS_STORAGE_BUCKET_NAME', '')
    AWS_ACCESS_KEY_ID = opts.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = opts.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_QUERYSTRING_AUTH = True
    AWS_DEFAULT_ACL = 'private'
    AWS_LOCATION = opts.get('AWS_LOCATION', '')

    # Thumbor
    THUMBOR_SERVER = opts.get('THUMBOR_SERVER', '')
    THUMBOR_MEDIA_URL = opts.get('THUMBOR_MEDIA_URL', '')
    THUMBOR_SECURITY_KEY = opts.get('THUMBOR_SECURITY_KEY', '')
    THUMBOR_ARGUMENTS = {
        "unsafe": opts.get('THUMBOR_UNSAFE', False),
    }
    THUMBOR_URL_REMOVE_UNSAFE = opts.get('THUMBOR_URL_REMOVE_UNSAFE', True)
    THUMBOR_MEDIA_URL_PREFIX = opts.get('THUMBOR_MEDIA_URL_PREFIX', '')

    # Rest framework
    # Note: is not possible define DEFAULT_FILTER_BACKENDS because there is some view
    # without queryset defined (retrieve, update views).
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PAGINATION_CLASS': 'bima_core.private_api.paginators.NumberPagination',
        'PAGE_SIZE': 20
    }

    # Swagger
    SWAGGER_SETTINGS = {
        'SHOW_REQUEST_HEADERS': True,
        'USE_SESSION_AUTH': True,
        'VALIDATOR_URL': None,
        'LOGIN_URL': 'admin:login',
        'LOGOUT_URL': 'admin:logout',
        'SECURITY_DEFINITIONS': None,
    }

    # Django Rest Auth
    REST_AUTH_SERIALIZERS = {
        'PASSWORD_RESET_SERIALIZER': 'private_api.serializers.PasswordResetSerializer'
    }

    # Flickr API Keys
    FLICKR_API_KEY = opts.get('FLICKR_API_KEY', '')
    FLICKR_SECRET_KEY = opts.get('FLICKR_SECRET_KEY', '')

    # Aux. File system storage
    FILE_SYSTEM_MEDIA_URL = opts.get('FILE_SYSTEM_MEDIA_URL', '/media/')

    # add photo type endpoint
    PHOTO_TYPES_ENABLED = opts.get('PHOTO_TYPES_ENABLED', True)

    # Drf Chunked Upload
    @property
    def DRF_CHUNKED_UPLOAD_STORAGE_CLASS(self):
        return file_system_storage

    DRF_CHUNKED_UPLOAD_PATH = opts.get('DRF_CHUNKED_UPLOAD_PATH', 'chunked_uploads/%Y/%m/%d')
    DRF_CHUNKED_UPLOAD_ABSTRACT_MODEL = True
    DRF_CHUNKED_UPLOAD_MAX_BYTES = opts.get('DRF_CHUNKED_UPLOAD_MAX_BYTES', 104857600)

    # RQ queues
    # Notes: use rq-dashboard to show queues and process (3rd party dependency)
    RQ_SHOW_ADMIN_LINK = True
    RQ_QUEUES = {
        # queue: upload
        # queue: haystack-photo-index
        RQ_UPLOAD_QUEUE: {
            "HOST": opts.get("DJANGO_RQ_DEFAULT_HOST", "localhost"),
            "PORT": opts.get("DJANGO_RQ_DEFAULT_PORT", 6379),
            "DB": opts.get("DJANGO_RQ_DEFAULT_DB", 0),
            "PASSWORD": opts.get("DJANGO_RQ_DEFAULT_PASS", ""),
            "DEFAULT_TIMEOUT": opts.get("DJANGO_RQ_DEFAULT_TIMEOUT", 500)
        },
        RQ_HAYSTACK_PHOTO_INDEX_QUEUE: {
            "HOST": opts.get("DJANGO_RQ_DEFAULT_HOST", "localhost"),
            "PORT": opts.get("DJANGO_RQ_DEFAULT_PORT", 6379),
            "DB": opts.get("DJANGO_RQ_DEFAULT_DB", 0),
            "PASSWORD": opts.get("DJANGO_RQ_DEFAULT_PASS", ""),
            "DEFAULT_TIMEOUT": opts.get("DJANGO_RQ_DEFAULT_TIMEOUT", 500)
        },
    }

    # Haystack for advanced searches
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': opts.get("DJANGO_HAYSTACK_ENGINE", 'haystack.backends.whoosh_backend.WhooshEngine'),
            'PATH': opts.get("DJANGO_HAYSTACK_ENGINE_PATH", "haystack_index"),
        },
    }
    ELASTICHSEARCH_ENGINE = 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine'
    if opts.get("DJANGO_HAYSTACK_ENGINE", "") == ELASTICHSEARCH_ENGINE:
        HAYSTACK_CONNECTIONS['default']["URL"] = opts.get("DJANGO_HAYSTACK_URL", 'http://bima-es:9200/')
        HAYSTACK_CONNECTIONS['default']["INDEX_NAME"] = opts.get("DJANGO_HAYSTACK_INDEX_NAME", 'haystack')

    HAYSTACK_DEFAULT_OPERATOR = opts.get("HAYSTACK_DEFAULT_OPERATOR", "OR")
    HAYSTACK_SIGNAL_PROCESSOR = 'bima_core.signals.PhotoSignalProcessor'


class Test(Base):
    """
    Project settings for testing.
    """
    try:
        from tests.generators import MOMMY_GEO_FIELDS
        MOMMY_CUSTOM_FIELDS_GEN = MOMMY_GEO_FIELDS
    except ImportError:
        pass

    # Override default storage to avoid save to S3
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = opts.get('TEST_MEDIA_ROOT', './tests/media/')

    # Override the base update index behaviour through signals
    # Note: skip queue update index task
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'

    def DATABASES(self):
        return self.get_databases(prefix='TEST_')

    LOG_LEVEL = 'ERROR'
