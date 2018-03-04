from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import Laptime
from .forms import CarForm, TrackForm


def laptimes(request):
    laptimes_with_diffs = []
    sectors = 0
    car_form = CarForm(request.GET or None)
    track_form = TrackForm(request.GET or None)
    if car_form.is_valid() and track_form.is_valid():
        track = track_form.cleaned_data['track']
        car = car_form.cleaned_data['car']
        laptimes = Laptime.objects.filter(track=track, car=car) \
                                  .order_by('user', 'time') \
                                  .distinct('user') \
                                  .values_list('id', flat=True)
        laptimes = Laptime.objects.filter(id__in=laptimes) \
                                  .order_by('time').all()
        for index, laptime in enumerate(laptimes):
            if index > 0:
                diff = laptime.diff_repr_from(laptimes[index-1])
            else:
                diff = 0
            laptimes_with_diffs.append((laptime, diff))
        sectors = track.sectors

        paginator = Paginator(laptimes_with_diffs, 10)
        page = request.GET.get('page')
        try:
            laptimes_with_diffs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            laptimes_with_diffs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            laptimes_with_diffs = paginator.page(paginator.num_pages)

    context = dict(laptimes=laptimes_with_diffs,
                   track_sectors=range(sectors),
                   forms=[car_form, track_form])
    return render(request, 'laptimes/laptimes.html', context=context)
