from django.shortcuts import render
from django.contrib.auth.models import User

from laptimes.models import Laptime


def index(request):
    laptimes = Laptime.objects.all()[:5]
    return render(request, 'index.html', context=dict(laptimes=laptimes))

def drivers(request):
    users = User.objects.all()
    return render(request, 'users.html', context=dict(users=users))
