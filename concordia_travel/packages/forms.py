from django import forms
from .models import Flight, Hotel, Activity

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'duration', 'price']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'phone_number', 'price']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'location', 'type', 'start_time', 'duration', 'price']
