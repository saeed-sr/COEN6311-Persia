from django import forms
from .models import Flight, Hotel, Activity, CustomPackage

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


class CustomPackageForm(forms.ModelForm):
    class Meta:
        model = CustomPackage
        fields = ['flights', 'hotels', 'activities']

    flights = forms.ModelMultipleChoiceField(
        queryset=Flight.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    hotels = forms.ModelMultipleChoiceField(
        queryset=Hotel.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
