import json

from django.shortcuts import render, get_object_or_404

from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from .models import Laptime, Car, Track
from .forms import LaptimesForm


def laptimes(request):
    sorted_laptimes, sectors = [], range(0)
    if request.method == 'GET':
        form = LaptimesForm()
    else:
        form = LaptimesForm(request.POST)
        if form.is_valid():
            track = get_object_or_404(Track, name=form.cleaned_data['track'])
            car = get_object_or_404(Car, name=form.cleaned_data['car'])
            laptimes = Laptime.objects.filter(track=track, car=car).all()
            sorted_laptimes = sorted(laptimes,
                                     key=lambda laptime: laptime.total_millis)
            sectors = range(track.sectors)
    return render(request, 'laptimes/laptimes.html',
                  context=dict(laptimes=sorted_laptimes, track_sectors=sectors,
                               form=form))


@token_required
def add(request):
    """Add a new laptime to the database."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            splits = [int(split) for split in data['splits']]
            track, car = data['track'], data['car']
        except (json.decoder.JSONDecodeError, ValueError):
            return JsonError('Bad data.')
        except KeyError as err:
            return JsonError('Missing <{}> argument.'.format(err.args[0]))

        track = get_object_or_404(Track, name=track)
        car = get_object_or_404(Car, name=car)

        laptime = Laptime(splits=splits, user=request.user, track=track,
                          car=car)
        laptime.save()
        return JsonResponse(dict(message='Lap time was saved.'))
    return JsonError('Only POST requests are allowed.')
