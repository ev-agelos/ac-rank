from django.conf.urls import include, url, static
from django.contrib import admin
from django.conf import settings

from . import views
from profiles import views as profile_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^drivers$', views.drivers, name='drivers'),
    url(r'', include('tokenapi.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/(?P<username>\w+)$', profile_views.profile, name='profile'),
    url(r'^laptimes/', include('laptimes.urls')),
    url(r'^api/laptimes/', include('laptimes.api.urls')),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static.static(settings.STATIC_URL,
                                 document_root=settings.STATIC_ROOT)
