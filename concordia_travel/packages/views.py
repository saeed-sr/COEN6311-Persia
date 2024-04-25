from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages

from django.db.models import Q
from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Flight, Hotel, Activity, CustomPackage, PreMadePackage,Question
from .forms import FlightForm, HotelForm, ActivityForm, CustomPackageForm, PreMadePackageForm
from django.contrib.auth.decorators import login_required ,user_passes_test

from django_tables2.views import SingleTableView
from .tables import FlightTable, HotelTable, ActivityTable
from booking.models import Booking

from .forms import CommentFlightForm
from .models import CommentFlight
from .forms import CommentHotelForm
from .models import CommentHotel
from .forms import QuestionForm



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

    def get_queryset(self):
        queryset = super().get_queryset()
        # ... existing sorting code ...

        # Search parameters
        departure_city = self.request.GET.get('departure_city', '')
        arrival_city = self.request.GET.get('arrival_city', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        # Filtering based on search parameters
        if departure_city:
            queryset = queryset.filter(departure_city__icontains=departure_city)
        if arrival_city:
            queryset = queryset.filter(arrival_city__icontains=arrival_city)
        if date_from and date_to:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            queryset = queryset.filter(departure_time__range=(date_from, date_to))

        return queryset

class HotelListView(BasePackageListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'
    table_class = HotelTable

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.GET.get('city', '')
        hotel_name = self.request.GET.get('hotel_name', '')

        if city:
            queryset = queryset.filter(city__icontains=city)
        if hotel_name:
            queryset = queryset.filter(name__icontains=hotel_name)

        return queryset

class ActivityListView(BasePackageListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    table_class = ActivityTable

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if date_from:
            queryset = queryset.filter(start_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(start_time__lte=date_to)

        return queryset

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
    comments = flight.comments.all()

    if request.method == 'POST':
        form = CommentFlightForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.flight = flight
            comment.save()
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page after posting a comment
    else:
        form = CommentFlightForm()

    return render(request, 'packages/flight_detail.html', {'flight': flight, 'comments': comments, 'comment_form': form})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    comments = hotel.comments.all()

    if request.method == 'POST':
        form = CommentHotelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.hotel = hotel
            comment.save()
            messages.success(request, 'Your comment has been added successfully.')
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page after posting a comment
    else:
        form = CommentHotelForm()

    return render(request, 'packages/hotel_detail.html', {'hotel': hotel, 'comments': comments, 'comment_form': form})


# views.py
from .forms import CommentActivityForm
from .models import CommentActivity

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    comments = activity.comments.all()

    if request.method == 'POST':
        form = CommentActivityForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.activity = activity
            comment.save()
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page after posting a comment
    else:
        form = CommentActivityForm()

    return render(request, 'packages/activity_detail.html', {'activity': activity, 'comments': comments, 'comment_form': form})


@login_required
def book_flight(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    custom_package = CustomPackage.objects.create(user=request.user)
    custom_package.flights.add(flight)
    Booking.objects.create(
        user=request.user,
        custom_package=custom_package,
        status='none'
    )
    messages.success(request, 'Flight added to your dashboard')
    return redirect('flight_detail', pk=pk)


@login_required
def book_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    custom_package = CustomPackage.objects.create(user=request.user)
    custom_package.hotels.add(hotel)
    Booking.objects.create(
        user=request.user,
        custom_package=custom_package,
        status='none'
    )
    messages.success(request, 'Hotel added to your dashboard')
    return redirect('hotel_detail', pk=pk)



@login_required
def book_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    custom_package = CustomPackage.objects.create(user=request.user)
    custom_package.activities.add(activity)
    Booking.objects.create(
        user=request.user,
        custom_package=custom_package,
        status='none'
    )
    messages.success(request, 'Activity added to your dashboard')
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

            Booking.objects.create(
            user=request.user,
            custom_package=custom_package,
            status='none'
    )

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


''''class PremadePackageListView(ListView):
    model = PreMadePackage
    template_name = 'packages/pre_made_package.html'
    context_object_name = 'premade_packages'
    '''

class PremadePackageListView(ListView):
    model = PreMadePackage
    template_name = 'packages/pre_made_package.html'
    context_object_name = 'premade_packages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_form'] = QuestionForm()  # Add the question form to the context
        return context

@login_required
def book_premade_package(request, pk):
    premade_package = get_object_or_404(PreMadePackage, pk=pk)
    custom_package = CustomPackage.objects.create(
        user=request.user, 
        agency=premade_package.agency
    )    
    # Assuming you want to copy details from the premade package to the custom package
    custom_package.flights.set(premade_package.flights.all())
    custom_package.hotels.set(premade_package.hotels.all())
    custom_package.activities.set(premade_package.activities.all())
    custom_package.save()

    # Create a booking record for the custom package
    Booking.objects.create(user=request.user, custom_package=custom_package, status='none')

    # Show a success message
    messages.success(request, "The premade package has been added to your dashboard.")

    # Redirect to a page where you can show the success message, for example, the dashboard
    return redirect('premade_packages')




def ask_question(request, package_id):
    # Retrieve the selected premade package
    package = PreMadePackage.objects.get(pk=package_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question associated with the selected premade package and the current user
            question = form.save(commit=False)
            question.user = request.user
            question.pre_made_package = package
            question.save()
            messages.success(request, 'Your question has been submitted successfully.')
            return redirect('premade_packages')  # Redirect to the premade packages page after submitting the question
    else:
        form = QuestionForm()
    return render(request, 'packages/premade_package.html', {'form': form, 'package': package})


def is_agent(user):
    return user.groups.filter(name='agents').exists()

@login_required
@user_passes_test(is_agent)
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        
        if form.is_valid():

            flight = form.save(commit=False)
            flight.agency = request.user
            flight.save()

            messages.success(request, 'Flight added successfully!')
            return redirect('agent_dashboard')  # Redirect to the agent dashboard or the appropriate URL
    else:
        form = FlightForm()

    return render(request, 'packages/add_flight.html', {'form': form})


@login_required
@user_passes_test(is_agent)
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.agency = request.user
            hotel.save()
            messages.success(request, 'Hotel added successfully!')
            return redirect('agent_dashboard')
    else:
        form = HotelForm()
    return render(request, 'packages/add_hotel.html', {'form': form})


@login_required
@user_passes_test(is_agent)
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.agency = request.user
            hotel.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('agent_dashboard')
    else:
        form = ActivityForm()
    return render(request, 'packages/add_activity.html', {'form': form}) 



@login_required
@user_passes_test(is_agent)
def add_premade_package(request):
    if request.method == 'POST':
        form = PreMadePackageForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            premade_package = form.save(commit=False)
            premade_package.agency = request.user
            premade_package.save()
            form.save_m2m()  # This is necessary for saving ManyToMany relationships
            messages.success(request, 'Premade Package added successfully!')
            return redirect('agent_dashboard')
    else:
        form = PreMadePackageForm(user=request.user)  # Pass the user to the form
    return render(request, 'packages/add_premade_package.html', {'form': form})