from django.contrib import admin

from .models import (
    Airport,
    Flight,
    FlightReservation,
    Vehicle
)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'created_at'
    )
    search_fields = ('name', 'location')
    ordering = ('-created_at',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'vehicle',
        'departure_airport',
        'destination_airport',
        'departure_time',
        'is_published',
        'created_at'
    )
    list_editable = (
        'vehicle',
        'departure_time',
        'is_published'
    )
    search_fields = ('number',)
    list_filter = (
        'vehicle',
        'departure_airport',
        'destination_airport',
        'is_published'
    )
    ordering = ('-created_at',)


@admin.register(FlightReservation)
class FlightReservationAdmin(admin.ModelAdmin):
    list_display = (
        'flight',
        'passenger_name',
        'seat_number',
        'phone_number',
        'created_at'
    )
    list_editable = ('seat_number',)
    search_fields = (
        'passenger_name',
        'phone_number'
    )
    list_filter = ('flight',)
    ordering = ('-created_at',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'vehicle_type',
        'capacity',
        'created_at'
    )
    list_editable = ('capacity',)
    search_fields = ('model',)
    list_filter = ('vehicle_type',)
    ordering = ('-created_at',)
