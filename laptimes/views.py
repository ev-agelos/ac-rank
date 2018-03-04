from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import Laptime
from .forms import CarForm, TrackForm


def laptimes(request):
    result, sectors = [], 0
    car_form = CarForm(request.GET or None)
    track_form = TrackForm(request.GET or None)
    if car_form.is_valid() and track_form.is_valid():
        track = track_form.cleaned_data['track']
        sectors = track.sectors
        car = car_form.cleaned_data['car']
        laptimes = Laptime.objects.filter(track=track, car=car) \
                                  .order_by('user', 'time') \
                                  .distinct('user')
        diffs = ['']  # no difference for the fastest laptime
        for index, laptime in enumerate(laptimes[1:], start=1):
            diff = laptime - laptimes[index-1]
            diffs.append('{:-6.3f}'.format(diff))

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

    context = dict(laptimes=result,
                   track_sectors=range(sectors),
                   forms=[car_form, track_form])
    return render(request, 'laptimes/laptimes.html', context=context)
