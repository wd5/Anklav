# -*- coding: utf-8 -*-
# Django settings for perspectiva project.
import os

APPEND_SLASH = False

ADMINS = (('Glader', 'glader.ru@gmail.com'),)

MANAGERS = (('Shyti', 'linashyti@gmail.com'),)

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'glader.ru@gmail.com'

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'core.Profile'

PROJECT_PATH = os.path.dirname(__file__)
FORCE_SCRIPT_NAME = ""

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-ru'
SITE_ID = 1
USE_I18N = True

DOMAIN = 'anklav-ekb.ru'
STATIC_ROOT = MEDIA_ROOT = PROJECT_PATH + '/static/'
STATIC_URL = MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin/media/'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
IS_DEVEL = True
TIMING = False

SECRET_KEY = '12345'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'))

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'messages.context_processors.inbox',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    'core.middleware.Prepare',
    'core.middleware.LogPost',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pytils',
    'south',
    'yafotki',
    'messages',

    'core',
    'news',
    'staticpage',
    'role_message',
    'contest',
)

LOG_PATH = '/var/log/projects/anklav'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-15s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'traceback.log'),
            'formatter': 'verbose',
            },
        'post': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'post.log'),
            'formatter': 'verbose',
            },
        'duels': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'duels.log'),
            'formatter': 'verbose',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'WARNING',
            'propagate': True,
            },
        'django.post': {
            'handlers': ['post'],
            'level': 'INFO',
            'propagate': True,
            },
        'django.duels': {
            'handlers': ['duels'],
            'level': 'INFO',
            'propagate': True,
            },
        }
}

ROLE_FIELDS = (
    ('tradition', u"Традиция", 6),
    ('special', u"Спецспособности", 5),
    ('actions', u"Акции", 5),
    ('actions_steal', u"Кража акции", 5),
    ('quest', u"Жизненный путь", 7),
    ('criminal', u"Связь с криминалом", 5),
    ('messages', u"Переписка", 5),
    )

TRADITION_FIELDS = (
    ('document', u"Один документ", 6),
    ('documents_list', u"Список документов", 8),
    ('tradition_questbook', u"Гостевая книга Традиции", 9),
    ('corporation_questbook', u"Гостевая книга корпорации/крим. структуры", 6),
    )

try:
    from local_settings import *
except ImportError:
    pass
