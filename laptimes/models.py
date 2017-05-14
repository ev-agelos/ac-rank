import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class Track(models.Model):

    ac_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    layout = models.CharField(max_length=50, null=True, blank=True)
    sectors = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        if self.layout:
            return self.name + ' ' + self.layout
        else:
            return self.name


class Car(models.Model):

    upgrades = (
        ('s1', 'Step1'),
        ('s2', 'Step2'),
        ('s3', 'Step3'),
        ('drift', 'Drift'),
        ('tuned', 'Tuned')
    )

    ac_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    upgrade = models.CharField(max_length=20, choices=upgrades, null=True,
                               blank=True)

    def __str__(self):
        return self.brand + ' ' + self.model


class Laptime(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    splits = ArrayField(models.PositiveIntegerField())
    time = models.PositiveIntegerField()
    track = models.ForeignKey(Track)
    car = models.ForeignKey(Car)

    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def millis_to_str(millis):
        timedelta = datetime.timedelta(milliseconds=millis)
        minutes = timedelta.seconds // 60
        seconds = timedelta.total_seconds() - (minutes * 60)
        return '{:02d}:{:06.3f}'.format(minutes, seconds)

    def splits_to_str(self):
        splits = []
        for milliseconds in self.splits:
            total_seconds = milliseconds / 1000
            minutes = int(total_seconds) // 60
            seconds = total_seconds - (minutes * 60)
            splits.append('{:01d}:{:06.3f}'.format(minutes, seconds))
        return splits

    def diff_repr_from(self, laptime):
        """Return the difference representation from another laptime."""
        millis = sum(self.splits) - sum(laptime.splits)
        seconds = millis / 1000
        return '{:-6.3f}'.format(seconds)

    def __str__(self):
        """Return the string represantation of the object."""
        return self.millis_to_str(self.time)


class LaptimeSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Laptime
        fields = ('splits', 'time')
