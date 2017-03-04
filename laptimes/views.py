import json

from django.shortcuts import render

from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from .models import Laptime


def laptimes(request):
    import pdb; pdb.set_trace()
    laptimes = Laptime.objects.all()
    return render(request, 'laptimes/laptimes.html',
                  context=dict(laptimes=laptimes))


@token_required
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if 'sector_times' in data:
            laptime = Laptime(sector_times=data['sector_times'],
                              user=request.user)
            laptime.save()
            return JsonResponse(dict(message='Lap time was saved.'))
        else:
            JsonError('No <sector_times> found in request payload.')
    return JsonError('Only POST requests are allowed.')
