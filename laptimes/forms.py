from django import forms

from .models import Car, Track


class LaptimesForm(forms.Form):

    brand = forms.ChoiceField(
        choices=[('', 'Select car')] + [
            (value, value)
            for value in Car.objects.values_list('brand', flat=True).distinct()]
    )
    model = forms.ChoiceField(
        choices=[('', 'Select model')] + [
            (value, value)
            for value in Car.objects.values_list('model', flat=True)]
    )

    track = forms.ChoiceField(
        choices=[('', 'Select track')] + [
            (value, value)
            for value in Track.objects.values_list('name', flat=True).distinct()]
    )

    layout = forms.TypedChoiceField(
        required=False,
        empty_value=None,
        choices=[('', 'Select layout')] + [
            (value, value)
            for value in Track.objects.exclude(layout=None)
            .values_list('layout', flat=True)]
    )
