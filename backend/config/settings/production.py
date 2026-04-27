from .base import *
from urllib.parse import urlparse

DEBUG = False

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    parsed_url = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed_url.path.lstrip('/'),
            'USER': parsed_url.username,
            'PASSWORD': parsed_url.password,
            'HOST': parsed_url.hostname,
            'PORT': parsed_url.port or '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://mondomaine.com',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True