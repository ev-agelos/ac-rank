"""Endpoints for the laptimes API."""

import json

from django.shortcuts import get_object_or_404
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from laptimes.models import Track, Car, Laptime, LaptimeSerialiser


@token_required
def get(request):
    """Return laptimes according to requested car/track combo."""
    if request.method != 'GET':
        return JsonError('Only GET method is allowed.')

    try:
        track = Track.objects.filter(circuit__name=request.GET['circuit'],
                                     layout=request.GET.get('layout'))
        car = Car.objects.filter(brand__name=request.GET['brand'],
                                 model=request.GET['model'])
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    if track is None or car is None:
        return JsonError('Track and/or car were not found.')

    serializer = LaptimeSerialiser(
        Laptime.objects.filter(car=car, track=track).all(),
        many=True
    )
    return JsonResponse(serializer.data, status=200)


@token_required
def add(request):
    """Add a new laptime to the database."""
    if request.method != 'POST':
        return JsonError('Only POST method is allowed.')
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

    laptime = Laptime(splits=splits, time=sum(splits), user=request.user,
                      track=track, car=car)
    laptime.save()
    return JsonResponse(dict(message='Lap time was saved.'))
