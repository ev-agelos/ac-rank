import json
from datetime import datetime

from django.shortcuts import render

from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from .models import Laptime


def laptimes(request):
    splits_list = Laptime.objects.all()
    splits_laptimes = []
    for splits in splits_list:
        laptime_in_ms = sum(splits.sector_times) / 1000
        date_from_splits = datetime.fromtimestamp(laptime_in_ms)
        laptime = ('{t.minute}:{t.second}:{t.microsecond}'
                   .format(t=date_from_splits))
        splits_laptimes.append((splits, laptime))
    return render(request, 'laptimes/laptimes.html',
                  context=dict(splits_laptimes=splits_laptimes))


@token_required
def add(request):
    """Add a new laptime to the database."""
    if request.method == 'POST':
        try:
            sector_times = json.loads(request.body.decode('utf-8'))['sector_times']
            if not all(map(str.isdigit, sector_times)):
                raise json.decoder.JSONDecodeError
        except KeyError:
            return JsonError('Missing <sector_times> argument.')
        except json.decoder.JSONDecodeError:
            return JsonError('Invalid argument <sector_times>.')

        laptime = Laptime(sector_times=sector_times, user=request.user)
        laptime.save()
        return JsonResponse(dict(message='Lap time was saved.'))
    return JsonError('Only POST requests are allowed.')
