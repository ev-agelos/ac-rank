import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

from .models import Laptime, Car, Track
from .forms import LaptimesForm


def laptimes(request):
    laptimes_with_diffs = []
    sectors = 0
    if not all([request.GET.get(arg) for arg in ('track', 'car')]):
        form = LaptimesForm()
        sectors = 0
    else:
        form = LaptimesForm(request.GET)
        if form.is_valid():
            track = get_object_or_404(Track, name=form.cleaned_data['track'])
            car = get_object_or_404(Car, name=form.cleaned_data['car'])
            laptimes = Laptime.objects.filter(track=track, car=car) \
                                      .order_by('user', 'time') \
                                      .distinct('user') \
                                      .values_list('id', flat=True)
            laptimes = Laptime.objects.filter(id__in=laptimes).order_by('time').all()
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
    context = dict(laptimes=laptimes_with_diffs, track_sectors=range(sectors),
                   form=form)
    return render(request, 'laptimes/laptimes.html', context=context)


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

        laptime = Laptime(splits=splits, time=sum(splits), user=request.user,
                          track=track, car=car)
        laptime.save()
        return JsonResponse(dict(message='Lap time was saved.'))
    return JsonError('Only POST requests are allowed.')
