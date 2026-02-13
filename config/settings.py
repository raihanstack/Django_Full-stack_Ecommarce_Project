import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
from urllib.parse import urlparse, parse_qsl

# Load .env file for environment variables
load_dotenv()

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True  # You can switch this to `False` in production
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Your app
    'cloudinary',  # Cloudinary app
    'cloudinary_storage',  # Cloudinary storage app
]

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Make sure templates are in the correct folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Middleware settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for auth
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for message handling
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'config.urls'  # Make sure this points to your URLs file

# Database configuration (PostgreSQL with the database URL)
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
        'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
    }
}

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where static files will be collected
STATICFILES_DIRS = [BASE_DIR / 'static']  # Your custom static files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Where media files will be uploaded
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': os.getenv("CLOUDINARY_API_KEY"),
    'API_SECRET': os.getenv("CLOUDINARY_API_SECRET"),
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# Email settings (using Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# SSLCommerz configuration
SSLCOMMERZ_STORE_ID = os.getenv("SSLCOMMERZ_STORE_ID")
SSLCOMMERZ_STORE_PASSWORD = os.getenv("SSLCOMMERZ_STORE_PASSWORD")
SSLCOMMERZ_CURRENCY = os.getenv("SSLCOMMERZ_CURRENCY")
SSLCOMMERZ_SUCCESS_URL = os.getenv("SSLCOMMERZ_SUCCESS_URL")
SSLCOMMERZ_FAIL_URL = os.getenv("SSLCOMMERZ_FAIL_URL")
SSLCOMMERZ_CANCEL_URL = os.getenv("SSLCOMMERZ_CANCEL_URL")
SSLCOMMERZ_IPN_URL = os.getenv("SSLCOMMERZ_IPN_URL")
