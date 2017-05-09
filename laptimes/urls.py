"""Url patterns for the laptimes package."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.laptimes, name='laptimes'),
]
