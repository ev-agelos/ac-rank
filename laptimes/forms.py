from django import forms

from .models import Car, Track, Laptime, User


class TrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['track'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Track.objects.all(),
            widget=forms.Select(attrs={'class':'custom-select'})
        )


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Car.objects.all(),
            widget=forms.Select(attrs={'class':'custom-select'})
        )


class UserTrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = tuple()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_track_ids = Laptime.objects.filter(user=user).values_list('track_id', flat=True)
        self.fields['track'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Track.objects.filter(id__in=user_track_ids),
            widget=forms.Select(attrs={'class':'custom-select'})
        )


class UserCarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = tuple()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_car_ids = Laptime.objects.filter(user=user).values_list('car_id', flat=True)
        self.fields['car'] = forms.ModelChoiceField(
            to_field_name='id',
            queryset=Car.objects.filter(id__in=user_car_ids),
            widget=forms.Select(attrs={'class':'custom-select'})
        )
