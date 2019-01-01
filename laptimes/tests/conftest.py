import os
import pytest

import django
from django.conf import settings
from django.test import Client
from django.test.client import RequestFactory


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ac_rank.settings.testing')
django.setup()


@pytest.fixture
def user(db):
    """Setup a user to use in tests."""
    from django.contrib.auth.models import User
    user = User.objects.create_user(username='foo', password=123)
    # overwrite attribute to use the original password in tests
    user.password = 123
    return user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def dj_request():
    return RequestFactory()
