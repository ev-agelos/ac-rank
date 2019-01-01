from .common import *

SECRET_KEY = 'really_secret_key'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'testing_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}
