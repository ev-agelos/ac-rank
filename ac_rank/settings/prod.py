import raven

from .common import *

DEBUG = False

STATIC_ROOT = "/var/www/ac-rank/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )

ALLOWED_HOSTS = ['*']  # should be configured by Nginx

SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000

RAVEN_CONFIG = {
    'dsn': '',  # NOTE set sentry dns in production
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
