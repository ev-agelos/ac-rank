from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Laptime(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sector_times = ArrayField(models.IntegerField())

    @property
    def time(self):
        return str(timedelta(seconds=sum(self.sector_times) / 1000))
