from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Flight, Hotel, Activity, CustomPackage, PreMadePackage
from .forms import FlightForm, HotelForm, ActivityForm, CustomPackageForm
from django.contrib.auth.decorators import login_required

from django_tables2.views import SingleTableView
from .tables import FlightTable, HotelTable, ActivityTable





# List views
class BasePackageListView(SingleTableView, ListView):
    template_name = None  # Update with your common template for package lists
    context_object_name = None  # Update with your common context variable name for package lists
    table_class = None  # Update with your common table class for package lists
    model = None  # Update with your common model for package lists
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get sorting parameters from the request
        sort = self.request.GET.get('sort', 'id')  # Default to sorting by ID if not specified
        order = self.request.GET.get('order', 'asc')

        # Apply sorting
        if order == 'asc':
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by(f'-{sort}')

        return queryset

class FlightListView(BasePackageListView):
    model = Flight
    template_name = 'packages/flight_list.html'
    context_object_name = 'flights'
    table_class = FlightTable

class HotelListView(BasePackageListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'
    table_class = HotelTable

class ActivityListView(BasePackageListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    table_class = ActivityTable

def flight_list(request):
    table = FlightTable(Flight.objects.all())
    return render(request, 'flight_list.html', {'table': table})

def hotel_list(request):
    table = HotelTable(Hotel.objects.all())
    return render(request, 'hotel_list.html', {'table': table})

def activity_list(request):
    table = ActivityTable(Activity.objects.all())
    return render(request, 'activity_list.html', {'table': table})


# Detail views
def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    return render(request, 'packages/flight_detail.html', {'flight': flight})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'packages/hotel_detail.html', {'hotel': hotel})

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'packages/activity_detail.html', {'activity': activity})


@login_required
def book_flight(request, pk):
    flight = get_object_or_404(Flight, pk=pk)

    # Add the booked flight to the user's custom package
    user_custom_package, created = CustomPackage.objects.get_or_create(user=request.user)
    user_custom_package.flights.add(flight)

    # Booking logic (e.g., create a Booking model)

    messages.success(request, 'Flight added to your custom package successfully!')
    return redirect('flight_detail', pk=pk)


@login_required
def book_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    # Add the booked flight to the user's custom package
    user_custom_package, created = CustomPackage.objects.get_or_create(user=request.user)
    user_custom_package.hotels.add(hotel)

    # Booking logic (e.g., create a Booking model)

    messages.success(request, 'Hotel added to your custom package successfully!')
    return redirect('hotel_detail', pk=pk)

@login_required
def book_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    # Add the booked flight to the user's custom package
    user_custom_package, created = CustomPackage.objects.get_or_create(user=request.user)
    user_custom_package.activities.add(activity)

    # Booking logic (e.g., create a Booking model)

    messages.success(request, 'activity added to your custom package successfully!')
    return redirect('activity_detail', pk=pk)


@login_required
def create_custom_package(request):
    if request.method == 'POST':
        form = CustomPackageForm(request.POST)
        if form.is_valid():
            custom_package = form.save(commit=False)
            custom_package.user = request.user
            custom_package.save()

            # Get the selected flights, hotels, and activities from the form
            selected_flights = form.cleaned_data['flights']
            selected_hotels = form.cleaned_data['hotels']
            selected_activities = form.cleaned_data['activities']

            # Add selected flights, hotels, and activities to the custom package
            custom_package.flights.add(*selected_flights)
            custom_package.hotels.add(*selected_hotels)
            custom_package.activities.add(*selected_activities)

            # Add success message
            messages.success(request, 'Your custom package has been added successfully.')

            return redirect('/')  # Change 'home' to the actual URL name of your homepage

    else:
        form = CustomPackageForm()

    context = {'form': form}

    # Check if there are messages and if it's the first time visiting the page after creating a package
    if messages.success and request.GET.get('created') == 'true' and form.is_valid():
        context['show_success_message'] = True

    return render(request, 'packages/create_custom_package.html', context)



class CustomPackageDetailView(DetailView):
    model = CustomPackage
    template_name = 'packages/custom_package_detail.html'
    context_object_name = 'custom_package'


class PremadePackageListView(ListView):
    model = PreMadePackage
    template_name = 'packages/pre_made_package.html'
    context_object_name = 'premade_packages'



def add_flight(request):
    pass