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


class Setup(models.Model):

    car = models.ForeignKey(Car)
    track = models.ForeignKey(Track)

    abs = models.SmallIntegerField(null=True)
    arb_front = models.SmallIntegerField(null=True)
    arb_rear = models.SmallIntegerField(null=True)
    brake_power_mult = models.SmallIntegerField(null=True)
    bump_stop_rate_lf = models.SmallIntegerField(null=True)
    bump_stop_rate_lr = models.SmallIntegerField(null=True)
    bump_stop_rate_rf = models.SmallIntegerField(null=True)
    bump_stop_rate_rr = models.SmallIntegerField(null=True)
    camber_lf = models.SmallIntegerField(null=True)
    camber_lr = models.SmallIntegerField(null=True)
    camber_rf = models.SmallIntegerField(null=True)
    camber_rr = models.SmallIntegerField(null=True)
    damp_bump_lf = models.SmallIntegerField(null=True)
    damp_bump_lr = models.SmallIntegerField(null=True)
    damp_bump_rf = models.SmallIntegerField(null=True)
    damp_bump_rr = models.SmallIntegerField(null=True)
    damp_fast_bump_lf = models.SmallIntegerField(null=True)
    damp_fast_bump_lr = models.SmallIntegerField(null=True)
    damp_fast_bump_rf = models.SmallIntegerField(null=True)
    damp_fast_bump_rr = models.SmallIntegerField(null=True)
    damp_fast_rebound_lf = models.SmallIntegerField(null=True)
    damp_fast_rebound_lr = models.SmallIntegerField(null=True)
    damp_fast_rebound_rf = models.SmallIntegerField(null=True)
    damp_fast_rebound_rr = models.SmallIntegerField(null=True)
    damp_rebound_lf = models.SmallIntegerField(null=True)
    damp_rebound_lr = models.SmallIntegerField(null=True)
    damp_rebound_rf = models.SmallIntegerField(null=True)
    damp_rebound_rr = models.SmallIntegerField(null=True)
    diff_coast = models.SmallIntegerField(null=True)
    diff_power = models.SmallIntegerField(null=True)
    engine_limiter = models.SmallIntegerField(null=True)
    final_ratio = models.SmallIntegerField(null=True)
    front_bias = models.SmallIntegerField(null=True)
    fuel = models.SmallIntegerField(null=True)
    internal_gear_2 = models.SmallIntegerField(null=True)
    internal_gear_3 = models.SmallIntegerField(null=True)
    internal_gear_4 = models.SmallIntegerField(null=True)
    internal_gear_5 = models.SmallIntegerField(null=True)
    internal_gear_6 = models.SmallIntegerField(null=True)
    internal_gear_7 = models.SmallIntegerField(null=True)
    packer_range_lf = models.SmallIntegerField(null=True)
    packer_range_lr = models.SmallIntegerField(null=True)
    packer_range_rf = models.SmallIntegerField(null=True)
    packer_range_rr = models.SmallIntegerField(null=True)
    pressure_lf = models.SmallIntegerField(null=True)
    pressure_lr = models.SmallIntegerField(null=True)
    pressure_rf = models.SmallIntegerField(null=True)
    pressure_rr = models.SmallIntegerField(null=True)
    rod_length_lf = models.SmallIntegerField(null=True)
    rod_length_lr = models.SmallIntegerField(null=True)
    rod_length_rf = models.SmallIntegerField(null=True)
    rod_length_rr = models.SmallIntegerField(null=True)
    spring_rate_lf = models.SmallIntegerField(null=True)
    spring_rate_lr = models.SmallIntegerField(null=True)
    spring_rate_rf = models.SmallIntegerField(null=True)
    spring_rate_rr = models.SmallIntegerField(null=True)
    toe_out_lf = models.SmallIntegerField(null=True)
    toe_out_lr = models.SmallIntegerField(null=True)
    toe_out_rf = models.SmallIntegerField(null=True)
    toe_out_rr = models.SmallIntegerField(null=True)
    traction_control = models.SmallIntegerField(null=True)
    tyres = models.SmallIntegerField(null=True)
    wing_1 = models.SmallIntegerField(null=True)
    wing_2 = models.SmallIntegerField(null=True)


class Laptime(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    splits = ArrayField(models.PositiveIntegerField(validators=[MinValueValidator(1)]),
                        validators=[MinLengthValidator(1)])
    time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    track = models.ForeignKey(Track)
    car = models.ForeignKey(Car)
    car_setup = models.ForeignKey(Setup, null=True, blank=True,
                                  on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __sub__(self, laptime):
        """Return the difference in time(millis) between two laptimes."""
        return self.time - laptime.time

    def __str__(self):
        """Return the string represantation of the object."""
        return str(to_laptime(self.time))


class LaptimeSerialiser(serializers.ModelSerializer):

    laptime = serializers.SerializerMethodField()

    class Meta:
        model = Laptime
        fields = ('splits', 'time', 'laptime')

    def get_laptime(self, obj):
        return to_laptime(obj.time)
