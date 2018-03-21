from django.contrib import admin

from .models import Laptime, Car, Track, CarSetup
# Register your models here.


class LaptimeAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'time', 'track', 'car')
    list_per_page = 25


class CarAdmin(admin.ModelAdmin):

    list_display = ('brand', 'model', 'upgrade')
    list_per_page = 25


class CarSetupAdmin(admin.ModelAdmin):

    list_display = ('id', 'car', 'track')
    list_per_page = 25


class TrackAdmin(admin.ModelAdmin):

    list_display = ('name', 'layout', 'sectors')
    list_per_page = 25


admin.site.register(Laptime, LaptimeAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarSetup, CarSetupAdmin)
admin.site.register(Track, TrackAdmin)
