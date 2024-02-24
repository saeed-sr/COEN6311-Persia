from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Flight, Hotel, Activity, CustomPackage
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

# Create views
# class FlightCreateView(CreateView):
#     model = Flight
#     form_class = FlightForm
#     template_name = 'flights/flight_form.html'

# class HotelCreateView(CreateView):
#     model = Hotel
#     form_class = HotelForm
#     template_name = 'hotels/hotel_form.html'

# class ActivityCreateView(CreateView):
#     model = Activity
#     form_class = ActivityForm
#     template_name = 'activities/activity_form.html'

# # Update views
# class FlightUpdateView(UpdateView):
#     model = Flight
#     form_class = FlightForm
#     template_name = 'flights/flight_form.html'

# class HotelUpdateView(UpdateView):
#     model = Hotel
#     form_class = HotelForm
#     template_name = 'hotels/hotel_form.html'

# class ActivityUpdateView(UpdateView):
#     model = Activity
#     form_class = ActivityForm
#     template_name = 'activities/activity_form.html'

# # Delete views
# class FlightDeleteView(DeleteView):
#     model = Flight
#     template_name = 'flights/flight_confirm_delete.html'
#     success_url = '/flights/'

# class HotelDeleteView(DeleteView):
#     model = Hotel
#     template_name = 'hotels/hotel_confirm_delete.html'
#     success_url = '/hotels/'

# class ActivityDeleteView(DeleteView):
#     model = Activity
#     template_name = 'activities/activity_confirm_delete.html'
#     success_url = '/activities/'



def book_flight(request, pk):
    # Here you would handle booking logic, such as saving to a Booking model
    # For now, let's just redirect to a confirmation page or back to the flight's detail page
    print("BOOKED FLIGHT", pk)
    return HttpResponseRedirect(reverse('flight_detail', args=[pk]))

def book_hotel(request, pk):
    # Here you would handle booking logic, such as saving to a Booking model
    # For now, let's just redirect to a confirmation page or back to the flight's detail page
    print("BOOKED HOTEL", pk)
    return HttpResponseRedirect(reverse('hotel_detail', args=[pk]))

def book_activity(request, pk):
    # Here you would handle booking logic, such as saving to a Booking model
    # For now, let's just redirect to a confirmation page or back to the flight's detail page
    print("BOOKED ACTIVITY", pk)
    return HttpResponseRedirect(reverse('activity_detail', args=[pk]))


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
    if messages.success and request.GET.get('created') == 'true':
        context['show_success_message'] = True

    return render(request, 'packages/create_custom_package.html', context)

class CustomPackageDetailView(DetailView):
    model = CustomPackage
    template_name = 'packages/custom_package_detail.html'
    context_object_name = 'custom_package'


class PremadePackageListView(ListView):
    pass
