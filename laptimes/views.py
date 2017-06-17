import json
from collections import defaultdict

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.aggregates.general import ArrayAgg

from .models import Laptime, Car, Track
from .forms import CarForm, TrackForm


def laptimes(request):
    laptimes_with_diffs = []
    sectors = 0
    car_form = CarForm(request.GET or None)
    track_form = TrackForm(request.GET or None)
    if car_form.is_valid() and track_form.is_valid():
        track = get_object_or_404(Track, name=track_form.cleaned_data['track'],
                                  layout=track_form.cleaned_data['layout'])
        car = get_object_or_404(Car,
                                brand=car_form.cleaned_data['brand'],
                                model=car_form.cleaned_data['model'],
                                upgrade=car_form.cleaned_data['upgrade'])
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

    cars = Car.objects.all()
    models_per_brand = defaultdict(set)
    upgrades_per_car = defaultdict(set)
    for car in cars:
        models_per_brand[car.brand].add(car.model)
        if car.upgrade is not None:
            upgrades_per_car[car.brand+car.model].add(car.upgrade)
    for key, value in models_per_brand.items():
        models_per_brand[key] = list(value)
    for key, value in upgrades_per_car.items():
        upgrades_per_car[key] = list(value)

    layouts_per_track = dict(
        Track.objects.exclude(layout=None).values('name')
        .annotate(layouts=ArrayAgg('layout'))
        .values_list('name', 'layouts'))

    context = dict(laptimes=laptimes_with_diffs,
                   track_sectors=range(sectors),
                   forms=[car_form, track_form],
                   models_per_brand=json.dumps(models_per_brand),
                   upgrades_per_car=json.dumps(upgrades_per_car),
                   layouts_per_track=json.dumps(layouts_per_track))
    return render(request, 'laptimes/laptimes.html', context=context)
