from .common import *

DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
