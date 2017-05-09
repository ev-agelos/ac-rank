"""Url patterns regarding the laptimes API."""

from django.conf.urls import url

from . import endpoints

urlpatterns = [
    url(r'^add$', endpoints.add, name='add-laptimes'),
    url(r'^get$', endpoints.get, name='get-laptimes'),
]
