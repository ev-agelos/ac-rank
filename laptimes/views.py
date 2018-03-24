import io
from configparser import ConfigParser

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from .templatetags.laptime_extras import to_laptime
from .models import Laptime, CarSetup
from .forms import CarForm, TrackForm, UserCarForm, UserTrackForm


def _get_laptimes(request, car_form, track_form, user=None):
    laptimes_with_diffs = []
    if car_form.is_valid() and track_form.is_valid():
        track = track_form.cleaned_data['track']
        car = car_form.cleaned_data['car']
        if user is not None:
            laptimes = Laptime.objects.filter(
                track=track, car=car, user_id=user.id
            ).order_by('time')
        else:
            laptimes = Laptime.objects.filter(
                track=track, car=car
            ).order_by('user', 'time').distinct('user')
        diffs = ['']  # no difference for the fastest laptime
        for index, laptime in enumerate(laptimes[1:], start=1):
            diff = laptime - laptimes[index-1]
            diffs.append(to_laptime(diff))

        laptimes_with_diffs = [(l, d) for l, d in zip(laptimes, diffs)]

    context = dict(laptimes=laptimes_with_diffs, forms=[car_form, track_form])
    return render(request, 'laptimes/laptimes.html', context=context)


def laptimes(request):
    """Return top laptimes."""
    car_form = CarForm(request.GET or None)
    track_form = TrackForm(request.GET or None)
    return _get_laptimes(request, car_form, track_form)


@login_required
def user_laptimes(request):
    """Return user's laptimes."""
    car_form = UserCarForm(request.user, request.GET or None)
    track_form = UserTrackForm(request.user, request.GET or None)
    return _get_laptimes(request, car_form, track_form, user=request.user)


@login_required
def download_setup(request, setup_id):
    setup = CarSetup.objects.get(pk=setup_id)

    config = ConfigParser()
    config.optionxform = str
    for field in setup._meta.get_fields():
        if field.name not in ('id', 'laptime', 'car', 'track'):
            value = getattr(setup, field.name, None)
            if value is not None:
                config[field.name.upper()] = {'VALUE': str(value)}
    config['CAR'] = {'MODEL': setup.car.ac_name}

    fob = io.StringIO(newline='\r\n')
    config.write(fob)
    fob.seek(0)
    data = fob.read()
    fob.close()

    name = 'setup__{}__{}.ini'.format(setup.car.ac_name, setup.track.ac_name)
    setup_file = ContentFile(data, name=name)
    response = HttpResponse(setup_file, 'text/plain')
    response['Content-Length'] = setup_file.size
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)

    return response
