import os
from datetime import timedelta

import dotenv
import logging.config
from pathlib import Path

# Базовые настройки приложения
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env.controller")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

PRODUCTION = True

ROOT_URLCONF = 'Config.urls'

FRONT_HOST = os.getenv('FRONT_HOST')

ALLOWED_HOSTS = ['server_id','127.0.0.1','localhost','host.docker.internal','web']

# Базовые настройки базы данных
DB_USER = os.getenv('DB_USER')

DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')

DB_HOST = os.getenv('DB_HOST')

DB_NAME = os.getenv('DB_NAME')

DB_PORT = os.getenv('DB_PORT')

CONN_MAX_AGE = None
# Базовые настройки Celery
RABBITMQ_DEFAULT_USER=os.getenv('RABBITMQ_DEFAULT_USER')

RABBITMQ_DEFAULT_PASS=os.getenv('RABBITMQ_DEFAULT_PASS')

# CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_BROKER_URL= f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit:5672/'

CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']

CELERY_TASK_SERIALIZER = 'pickle'

CELERY_RESULT_SERIALIZER = 'pickle'

CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_TIMEZONE = "Europe/Moscow"

CELERY_CACHE_BACKEND = 'default'

CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_CREATE_MISSING_QUEUES = True

CELERYD_MAX_TASKS_PER_CHILD = 1

CELERY_BROKER_CONNECTION_RETRY = True

CELERY_DISABLE_RATE_LIMITS = True

CELERY_BROKER_CONNECTION_MAX_RETRIES = 400

# Дополнительные базовые настройки
ADMINS = [
    {
        'ADMIN_NAME': os.getenv('ADMIN_NAME'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL'),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD'),
    }
]

# Установленные приложения
INSTALLED_APPS = [
    'api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
]

# Програмное обеспечение
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


# Настройка запуска приложения
ASGI_APPLICATION = 'Config.asgi.application'

# Настройка базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_USER_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Настройки языка и времени
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Настройка медиафайлов и статики
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/data/'

MEDIA_ROOT = os.path.join(BASE_DIR, "data")

# Настройки CORS заголовков
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Настройки DRF
REST_FRAMEWORK = {
    # Права доступа поумолчанию
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Настройки шаблонизатора
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Настройка логирования
LOGGING_CONFIG = None

LOGLEVEL = os.getenv('DJANGO_LOGLEVEL').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
    },
})

