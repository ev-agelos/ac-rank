"""Endpoints for the laptimes API."""

import logging
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
        track = Track.objects.filter(ac_name=request.GET['track'],
                                     layout=request.GET.get('layout'))
        car = Car.objects.filter(ac_name=request.GET['car'])
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    if track is None or car is None:
        msg = 'Track and/or car were not found.'
        logger = logging.getLogger(__name__)
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)

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
    logger = logging.getLogger(__name__)
    try:
        data = json.loads(request.body.decode('utf-8'))
        splits = [int(split) for split in data['splits']]
        track, layout, car = data['track'], data.get('layout'), data['car']
    except json.decoder.JSONDecodeError:
        msg = "Bad data. Can't load track."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)
    except ValueError:
        msg = "Bad data. Can't cast split to integer."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    track = get_object_or_404(Track, ac_name=track, layout=layout)
    if len(splits) != track.sectors:  # Validate splits
        msg = "Bad data. Number of splits differs from track's."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)
    car = get_object_or_404(Car, ac_name=car)

    laptime = Laptime(splits=splits, time=sum(splits), user=request.user,
                      track=track, car=car)
    laptime.save()
    return JsonResponse(dict(message='Lap time was saved.'))
