import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment detection
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEVELOPMENT').upper()
PRODUCTION = ENVIRONMENT == 'PRODUCTION'
DEVELOPMENT = ENVIRONMENT == 'DEVELOPMENT'

# SECURITY WARNING: keep the secret key used in production secret!
if PRODUCTION:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required in production")
else:
    SECRET_KEY = 'django-insecure-xh_y-46bl2qmg!mkb9b#089@0ci!l2$61+c9^)y$5^)nb_s1gh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOPMENT

# Allowed hosts configuration
if PRODUCTION:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
        raise ValueError("ALLOWED_HOSTS environment variable is required in production")
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.48']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'accueil',
    'blog',
    'flow',
    'rest_framework',
    'spectacle',
    'corsheaders',  # Add CORS headers app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware - must be above CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
if PRODUCTION:
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = False
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://192.168.1.48:3000",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

ROOT_URLCONF = 'rolwebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rolwebsite.wsgi.application'

# Database configuration
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'rolwebsite'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'postgres'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Configuration
if PRODUCTION:
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'AUTH_HEADER_TYPES': ('Bearer',),
    }
else:
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'AUTH_HEADER_TYPES': ('Bearer',),
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

os.makedirs(MEDIA_ROOT, exist_ok=True)

# File upload settings
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Allowed file types and sizes
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/avi']
ALLOWED_AUDIO_TYPES = ['audio/mp3', 'audio/wav', 'audio/ogg']
ALLOWED_FILE_TYPES = ['application/pdf', 'text/plain', 'application/msword']

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB for videos/files
MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10MB for images
FILE_UPLOAD_TIMEOUT = 300  # seconds

# Security settings for production
if PRODUCTION:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = False  # Set to True if using HTTPS
    SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
    CSRF_COOKIE_SECURE = False  # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
else:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration for production
if PRODUCTION:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/app/logs/django.log',
                'formatter': 'verbose',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }