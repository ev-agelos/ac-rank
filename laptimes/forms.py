from django import forms

from .models import Car, Track


class LaptimesForm(forms.Form):

    car = forms.ModelChoiceField(queryset=Car.objects.all(), required=True)
    track = forms.ModelChoiceField(queryset=Track.objects.all(), required=True)
