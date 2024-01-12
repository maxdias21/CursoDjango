# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from .environment import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
