from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .templatetags.laptime_extras import to_laptime
from .models import Laptime
from .forms import CarForm, TrackForm, UserCarForm, UserTrackForm


def _get_laptimes(request, car_form, track_form, user=None):
    result = []
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
        paginator = Paginator(laptimes_with_diffs, 10)
        try:
            result = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)

    context = dict(laptimes=result, forms=[car_form, track_form])
    return render(request, 'laptimes/laptimes.html', context=context)


def laptimes(request):
    """Return top laptimes."""
    car_form = CarForm(request.GET or None)
    track_form = TrackForm(request.GET or None)
    return _get_laptimes(request, car_form, track_form)


def user_laptimes(request):
    """Return user's laptimes."""
    car_form = UserCarForm(request.user, request.GET or None)
    track_form = UserTrackForm(request.user, request.GET or None)
    return _get_laptimes(request, car_form, track_form, user=request.user)
