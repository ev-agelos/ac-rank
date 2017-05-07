from django.contrib import admin

from .models import Laptime, Car, Brand, Track, Circuit
# Register your models here.


class LaptimeAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'splits', 'track', 'car')
    list_per_page = 25


class BrandAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_per_page = 25


class CarAdmin(admin.ModelAdmin):

    list_display = ('id', 'brand', 'model')
    list_per_page = 25


class CircuitAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_per_page = 25


class TrackAdmin(admin.ModelAdmin):

    list_display = ('id', 'circuit', 'layout', 'sectors')
    list_per_page = 25


admin.site.register(Laptime, LaptimeAdmin)

admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)

admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Track, TrackAdmin)
