from .base import *

DEBUG = True

TEST_MODE = True

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'nanny_db'),
        'USER': os.environ.get('POSTGRES_USER', 'ofs'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'ofs'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432')
    }
}
