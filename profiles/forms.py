from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('country', )
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'custom-select'})
        }
