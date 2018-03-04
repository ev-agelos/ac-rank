from django import forms

from .models import Car, Track


class TrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['track'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Track.objects.all()
        )


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Car.objects.all()
        )
