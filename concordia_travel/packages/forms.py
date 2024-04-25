from django import forms
from .models import Flight, Hotel, Activity, CustomPackage,CommentFlight, PreMadePackage, CommentHotel, CommentActivity,Question

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
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

    hotels = forms.ModelMultipleChoiceField(
        queryset=Hotel.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

class PreMadePackageForm(forms.ModelForm):
    class Meta:
        model = PreMadePackage  # Ensure this matches your PreMadePackage model
        fields = ['flights', 'hotels', 'activities']
        widgets = {
            'flights': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'hotels': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'activities': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super(PreMadePackageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['flights'].queryset = Flight.objects.filter(agency=user)
            self.fields['hotels'].queryset = Hotel.objects.filter(agency=user)
            self.fields['activities'].queryset = Activity.objects.filter(agency=user)
    

class CommentFlightForm(forms.ModelForm):
    class Meta:
        model = CommentFlight
        fields = ['text']


class CommentHotelForm(forms.ModelForm):
    class Meta:
        model = CommentHotel
        fields = ['text']

class CommentActivityForm(forms.ModelForm):
    class Meta:
        model = CommentActivity
        fields = ['text']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']