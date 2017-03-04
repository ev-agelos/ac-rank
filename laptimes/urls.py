"""Url patterns for the laptimes package."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add$', views.add, name='add-laptimes'),
    url(r'^$', views.laptimes, name='laptimes'),
]
