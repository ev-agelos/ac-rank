from .common import *


SECRET_KEY = 'really_secret_key'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
