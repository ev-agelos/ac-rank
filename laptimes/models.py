import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Track(models.Model):

    name = models.CharField(max_length=100)
    sectors = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def humanize(self):
        pass

    def __str__(self):
        return self.name


class Car(models.Model):

    upgrades = (
        ('s1', 'Step1'),
        ('s2', 'Step2'),
        ('s3', 'Step3'),
        ('drift', 'Drift'),
        ('dtm', 'Gr.A 92'),
        ('gra', 'Group A'),
        ('tuned', 'Tuned')
    )

    name = models.CharField(max_length=100)
    upgrade = models.CharField(max_length=20, choices=upgrades, null=True,
                               blank=True)

    def humanize(self):
        pass

    def __str__(self):
        return self.name


class Laptime(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    splits = ArrayField(models.PositiveIntegerField())
    track = models.ForeignKey(Track)
    car = models.ForeignKey(Car)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time(self):
        timedelta = datetime.timedelta(seconds=sum(self.splits) / 1000)
        minutes = int(timedelta.total_seconds() // 60)  # remove floating
        seconds = int(timedelta.seconds)  # remove floating
        milliseconds = timedelta.microseconds // 1000
        return '{}:{}.{:03d}'.format(minutes, seconds, milliseconds)

    def __str__(self):
        return self.time
