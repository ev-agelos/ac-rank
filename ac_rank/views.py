from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def drivers(request):
    users = User.objects.all()
    return render(request, 'users.html', context=dict(users=users))
