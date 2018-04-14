"""Endpoints for the laptimes API."""

import logging
import json

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from laptimes.models import Track, Car, Laptime, Setup, LaptimeSerialiser


@token_required
def get(request):
    """Return laptimes according to requested car/track combo."""
    if request.method != 'GET':
        return JsonError('Only GET method is allowed.')

    try:
        track = Track.objects.filter(ac_name=request.GET['track'],
                                     layout=request.GET.get('layout') or '')
        car = Car.objects.filter(ac_name=request.GET['car'])
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    if track.count() == 0 or car.count() == 0:
        msg = 'Track and/or car were not found.'
        logger = logging.getLogger(__name__)
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)

    serializer = LaptimeSerialiser(
        Laptime.objects.filter(car=car, track=track).order_by('user', 'time') \
                                                    .distinct('user'),
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
    except json.decoder.JSONDecodeError:
        msg = "Bad data. Can't load parameters."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)

    try:
        track, car, splits = data['track'], data['car'], data['splits']
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    try:
        splits = [int(split) for split in splits]
    except ValueError:
        msg = "Bad data. Can't cast split to integer."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)

    car = get_object_or_404(Car, ac_name=car)
    track = get_object_or_404(Track, ac_name=track,
                              layout=data.get('layout') or '')
    if track.sectors is not None:
        if len(splits) != track.sectors:  # Validate splits
            msg = "Bad data. Number of splits differs from track's."
            logger.warning(msg, exc_info=True, extra={'request': request})
            return JsonError(msg)
    else:
        track.sectors = len(splits)
        track.save()

    car_setup = data.get('car_setup')
    if car_setup is not None:
        car_setup, created = Setup.objects.get_or_create(
            car=car,
            track=track,
            **data['car_setup']
        )

    laptime = Laptime(splits=splits, time=sum(splits), user=request.user,
                      track=track, car=car, car_setup=car_setup)
    try:
        laptime.full_clean()
    except ValidationError as err:
        return JsonError('Bad data. ' + str(err))

    laptime.save()
    return JsonResponse(dict(
        message='Lap time was saved.',
        laptime_id=laptime.id
    ))


@token_required
def add_setup(request):
    """Add a new setup to an existing laptime."""
    if request.method != 'POST':
        return JsonError('Only POST method is allowed.')
    logger = logging.getLogger(__name__)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        msg = "Bad data. Can't load parameters."
        logger.warning(msg, exc_info=True, extra={'request': request})
        return JsonError(msg)

    try:
        setup, laptime_id = data['car_setup'], data['laptime_id']
    except KeyError as err:
        return JsonError('Missing <{}> argument.'.format(err.args[0]))

    try:
        laptime = Laptime.objects.get(pk=laptime_id)
    except Laptime.DoesNotExist:
        return JsonError('Laptime not found')

    if laptime.car_setup is not None:
        return JsonError('Setup already exists for the laptime.')

    car_setup, created = Setup.objects.get_or_create(
        car=laptime.car,
        track=laptime.track,
        **setup
    )
    laptime.car_setup = car_setup
    laptime.save()
    return JsonResponse(dict(message='Setup was saved for the laptime.'))
