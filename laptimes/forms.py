from django import forms

from .models import Brand, Car, Track, Circuit


class LaptimesForm(forms.Form):

    brand = forms.ChoiceField(
        choices=[('', 'Select car')] + [
            (value, value)
            for value in Brand.objects.values_list('name', flat=True)]
    )
    model = forms.ChoiceField(
        choices=[('', 'Select car model')] + [
            (value, value)
            for value in Car.objects.values_list('model', flat=True)]
    )

    circuit = forms.ChoiceField(
        choices=[('', 'Select track')] + [
            (value, value)
            for value in Circuit.objects.values_list('name', flat=True)]
    )

    layout = forms.TypedChoiceField(
        required=False,
        empty_value=None,
        choices=[('', 'Select track layout')] + [
            (value, value)
            for value in Track.objects.exclude(layout=None)
            .values_list('layout', flat=True)]
    )
