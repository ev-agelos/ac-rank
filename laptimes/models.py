import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from rest_framework import serializers

from laptimes.templatetags.laptime_extras import to_laptime

class Track(models.Model):

    class Meta:
        unique_together = ('ac_name', 'layout')

    ac_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    layout = models.CharField(max_length=50, default='', blank=True)
    sectors = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        if self.layout:
            return self.name.title() + ' ' + self.layout
        else:
            return self.name.title()


class Car(models.Model):

    upgrades = (
        ('s1', 'Step 1'),
        ('s2', 'Step 2'),
        ('s3', 'Step 3'),
        ('drift', 'Drift'),
        ('tuned', 'Tuned')
    )

    ac_name = models.CharField(max_length=200, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    upgrade = models.CharField(max_length=20, choices=upgrades, null=True,
                               blank=True)

    def __str__(self):
        car = self.brand.title() + ' ' + self.model.upper()
        if self.upgrade is not None:
            car += ' ' + self.upgrade.title()
        return car


class Laptime(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    splits = ArrayField(models.PositiveIntegerField(validators=[MinValueValidator(1)]),
                        validators=[MinLengthValidator(1)])
    time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    track = models.ForeignKey(Track)
    car = models.ForeignKey(Car)

    created_at = models.DateTimeField(auto_now_add=True)

    def __sub__(self, laptime):
        """Return the difference in time(millis) between two laptimes."""
        return self.time - laptime.time

    def __str__(self):
        """Return the string represantation of the object."""
        return str(to_laptime(self.time))


class LaptimeSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Laptime
        fields = ('splits', 'time')
