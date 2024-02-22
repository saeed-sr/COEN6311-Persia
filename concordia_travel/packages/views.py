from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Flight, Hotel, Activity
from .forms import FlightForm, HotelForm, ActivityForm

# List views
class FlightListView(ListView):
    model = Flight
    template_name = 'flight_list.html'
    context_object_name = 'flights'

class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'

class ActivityListView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'

# Detail views
class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'

# Create views
class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flights/flight_form.html'

class HotelCreateView(CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotels/hotel_form.html'

class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'

# Update views
class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flights/flight_form.html'

class HotelUpdateView(UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotels/hotel_form.html'

class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'

# Delete views
class FlightDeleteView(DeleteView):
    model = Flight
    template_name = 'flights/flight_confirm_delete.html'
    success_url = '/flights/'

class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = 'hotels/hotel_confirm_delete.html'
    success_url = '/hotels/'

class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = '/activities/'
