import os
# Django settings for kingdoms project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ERROR_FILE = ''

BASE_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/..")

ADMINS = (
    ('Neamar', 'kingdoms@neamar.fr'),
)

MANAGERS = ADMINS

DATABASES = {}

if os.getenv('DB') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'kingdoms',
            'USER': 'postgres',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite'
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASE_DIR + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

LOGIN_URL = 'django.contrib.auth.views.login'
LOGIN_REDIRECT_URL = 'kingdom.views.index.app'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = BASE_DIR + '/collected-static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')e$l_21#m6rtwwhmf#fo34=%gv&amp;4=hc$h^atvyiy()&amp;tgcij6j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_DIR + '/templates',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'HEADER_DATE_FORMAT': 'j F Y',
    'SEARCH_URL': '/admin/event/event',
    'LIST_PER_PAGE': 50,
    'MENU': (
        {
            'label': 'Scripting',
            'icon': 'icon-star-empty',
            'models': ('event.event', 'mission.mission', 'kingdom.quality', 'internal.recurring')
        },
        {
            'label': 'Pending',
            'icon': 'icon-time',
            'models': ('event.pendingevent', 'mission.pendingmission')
        },
        '-',
        {
            'app': 'kingdom',
            'models': ('kingdom', 'folk', 'message', 'claim', 'quality', 'qualitycategory')
        },
        {
            'app': 'event',
            'models': ('event', 'eventcategory', 'pendingevent', 'pendingeventtoken')
        },
        {
            'app': 'mission',
            'models': ('mission', 'availablemission', 'pendingmission')
        },
        'internal',
        {
            'app': 'title',
            'models': ('title', 'availabletitle')
        },
        'bargain',
        'reporting',
        '-',
        {
            'app': 'auth',
            'icon': 'icon-user'
        },
        {
            'app': 'admin',
            'icon': 'icon-lock'
        },
    )
}

FIXTURE_DIRS = (
    BASE_DIR + '/config/fixtures/',
)

# Disable migrations and use syncdb for tests.
SOUTH_TESTS_MIGRATE = False

INSTALLED_APPS = (
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Pip Lib
    'south',
    #'django_extensions',

    # Kingdom apps
    'kingdom',
    'title',
    'internal',
    'mission',
    'event',
    'bargain',
    'reporting',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
