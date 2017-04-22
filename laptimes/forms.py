from django import forms

from .models import Car, Track


class LaptimesForm(forms.Form):

    car = forms.ModelChoiceField(queryset=Car.objects.all(),
                                 required=True,
                                 to_field_name='name',
                                 empty_label='Select car')
    track = forms.ModelChoiceField(queryset=Track.objects.all(),
                                   required=True,
                                   to_field_name='name',
                                   empty_label='Select track')
