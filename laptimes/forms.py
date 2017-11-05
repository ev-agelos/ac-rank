from django import forms

from .models import Car, Track


class TrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['track'] = forms.ModelChoiceField(
            to_field_name='name',
            queryset=Track.objects.values_list('name', flat=True).distinct()
        )
        self.fields['layout'] = forms.ModelChoiceField(
            to_field_name='layout',
            required=False,
            queryset=Track.objects.values_list('layout', flat=True).distinct()
        )


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ('brand', 'model', 'upgrade')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'] = forms.ModelChoiceField(
            to_field_name='brand',
            queryset=Car.objects.values_list('brand', flat=True).distinct()
        )
        self.fields['model'] = forms.ModelChoiceField(
            to_field_name='model',
            queryset=Car.objects.values_list('model', flat=True).distinct()
        )
