from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Flight, Hotel, Activity, CustomPackage, PreMadePackage
from .forms import FlightForm, HotelForm, ActivityForm, CustomPackageForm
from django.contrib.auth.decorators import login_required




# List views
class FlightListView(ListView):
    model = Flight
    template_name = 'packages/flight_list.html'
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