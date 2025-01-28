from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

from .models import FlightReservation, Flight


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class FlightReservationForm(forms.ModelForm):
    class Meta:
        model = FlightReservation
        fields = ["passenger_name", "seat_number", "phone_number"]


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = (
            'number',
            'vehicle',
            'destination_airport',
            'departure_airport',
            'departure_time',
            'arrival_time',
            'status'
        )
        widgets = {
            'vehicle': forms.Select(),
            'destination_airport': forms.Select(),
            'departure_airport': forms.Select(),
            'status': forms.Select(),
            'departure_time': forms.DateTimeInput(attrs={"type": "datetime-local"}, format='%d-%m-%YT%H:%M'),
            'arrival_time': forms.DateTimeInput(attrs={"type": "datetime-local"}, format='%d-%m-%YT%H:%M'),
        }
