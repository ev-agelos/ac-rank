from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'', include('tokenapi.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^laptimes/', include('laptimes.urls')),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]