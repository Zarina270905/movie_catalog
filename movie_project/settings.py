"""
Django settings for movie_project project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ============================================

SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# ============================================
# НАСТРОЙКИ ПРИЛОЖЕНИЙ
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # ваше приложение
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

ROOT_URLCONF = 'movie_project.urls'

# ============================================
# НАСТРОЙКИ ШАБЛОНОВ
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'movie_project.wsgi.application'

# ============================================
# НАСТРОЙКИ БАЗЫ ДАННЫХ
# ============================================

DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / config('DB_NAME', default='db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default=''),
        }
    }

# ============================================
# ВАЛИДАЦИЯ ПАРОЛЕЙ
# ============================================

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

# ============================================
# МЕЖДУНАРОДНЫЕ НАСТРОЙКИ
# ============================================

LANGUAGE_CODE = config('LANGUAGE_CODE', default='ru-ru')
TIME_ZONE = config('TIME_ZONE', default='Europe/Moscow')
USE_I18N = True
USE_TZ = True

# ============================================
# СТАТИЧЕСКИЕ ФАЙЛЫ
# ============================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# НАСТРОЙКИ ПО УМОЛЧАНИЮ
# ============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# НАСТРОЙКИ АУТЕНТИФИКАЦИИ
# ============================================

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# ============================================
# EMAIL НАСТРОЙКИ (ДЛЯ ВЕРИФИКАЦИИ)
# ============================================

EMAIL_BACKEND = config('EMAIL_BACKEND',
                      default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL',
                           default='noreply@moviecatalog.com')

# ============================================
# БЕЗОПАСНОСТЬ
# ============================================

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS',
                             default='http://localhost:8000,http://127.0.0.1:8000').split(',')

# ============================================
# КАСТОМНЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ
# ============================================

SITE_NAME = config('SITE_NAME', default='MovieCatalog')
SITE_DOMAIN = config('SITE_DOMAIN', default='localhost:8000')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@moviecatalog.com')

# ============================================
# ЛОГИРОВАНИЕ
# ============================================

LOG_LEVEL = config('LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}