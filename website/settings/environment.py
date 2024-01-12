from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&-ev-8q(+(mgf77-=1f12sy5+9box$3e#7pj%^#cjudzd8sj5*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
