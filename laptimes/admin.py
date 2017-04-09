from django.contrib import admin

from .models import Laptime, Car, Track
# Register your models here.


class LaptimeAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'splits', 'track', 'car')
    list_per_page = 25


class CarAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'upgrade')
    list_per_page = 25


class TrackAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'sectors')
    list_per_page = 25


admin.site.register(Laptime, LaptimeAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Track, TrackAdmin)
