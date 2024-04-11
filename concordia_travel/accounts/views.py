from django.http import JsonResponse
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from packages.models import Question, Flight, Hotel, Activity, CustomPackage, PreMadePackage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Sum, Count
from datetime import datetime
from packages.models import PreMadePackage
from booking.models import Booking
from django.db.models import Q
from django.utils.timezone import now
from notifications.models import Notification
from notifications.signals import notify



# from django.contrib.auth import update_password



# Create your views here.


def register(request):

    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()

                user.groups.add(Group.objects.get(name='normal_users'))

                print('User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html') 
    

def login(request):
    if request.method == 'POST':
        print('Login method')
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print('User is not none')
            auth.login(request, user)
            return redirect('/')
        else:
            print('User is none')
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/')




@login_required
def user_dashboard(request):
    # Retrieve questions associated with the current user
    user_questions = Question.objects.filter(user=request.user)
    # Get the count of unread notifications for the current user
    unread_notifications_count = Notification.objects.unread().filter(recipient=request.user).count()

    context = {
        'user_questions': user_questions,
        'unread_notifications_count': unread_notifications_count,
    }

    return render(request, 'accounts/dashboard.html', context)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

            # Password change logic
            if 'password1' in request.POST:  # Check if new password is provided
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Your profile and password have been updated!')
                else:
                    messages.error(request, 'Passwords do not match!')
            else:
                # Profile update without password change
                messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/edit_profile.html', context)



def is_agent(user):
    return user.groups.filter(name='agents').exists()


@login_required
@user_passes_test(is_agent)
def agent_dashboard(request):
    current_month = now().month
    current_year = now().year

    # Get all premade packages created by the agent
    premade_packages = PreMadePackage.objects.filter(agency=request.user)

    # Calculate total and monthly revenue
    total_revenue, monthly_revenue = 0, 0
    current_month = datetime.now().month
    package_data = []

    for package in premade_packages:
        bookings = Booking.objects.filter(
            Q(custom_package__flights__in=package.flights.all()) | 
            Q(custom_package__hotels__in=package.hotels.all()) | 
            Q(custom_package__activities__in=package.activities.all()),
            custom_package__agency=request.user
        ).distinct()

        booking_count = bookings.count()
        revenue = sum(booking.custom_package.get_total_price() for booking in bookings)
        monthly_bookings = bookings.filter(date_created__month=current_month)
        monthly_revenue += sum(booking.custom_package.get_total_price() for booking in monthly_bookings)
        total_revenue += revenue

        # Get the user details from the bookings
        users_booked = bookings.values_list('user__username', 'user__first_name', 'user__last_name', 'user__email').distinct()

        # Convert the query result to a list of dictionaries
        users_details = [{'username': user[0], 'first_name': user[1], 'last_name': user[2], 'email': user[3]} for user in users_booked]

        package_data.append({
            'package': package,
            'booking_count': booking_count,
            'revenue': revenue,
            'users_details': users_details  # Add the users details to the package data
        })

    # Fetch flights, hotels, and activities added by the agent
    flights_data = Flight.objects.filter(agency=request.user)
    hotels_data = Hotel.objects.filter(agency=request.user)
    activities_data = Activity.objects.filter(agency=request.user)


    # Calculate the bookings and revenue for each type of product
    flights_booking_data = [
        {
            'flight': flight,
            'booking_count': flight.custompackage_set.count(),
            'revenue': sum(booking.get_total_price() for booking in flight.custompackage_set.all())
        }
        for flight in flights_data
    ]

    hotels_booking_data = [
        {
            'hotel': hotel,
            'booking_count': hotel.custompackage_set.count(),
            'revenue': sum(booking.get_total_price() for booking in hotel.custompackage_set.all())
        }
        for hotel in hotels_data
    ]

    activities_booking_data = [
        {
            'activity': activity,
            'booking_count': activity.custompackage_set.count(),
            'revenue': sum(booking.get_total_price() for booking in activity.custompackage_set.all())
        }
        for activity in activities_data
    ]

    # Fetch flights, hotels, and activities added by the agent
    agent_flights = Flight.objects.filter(agency=request.user)
    agent_hotels = Hotel.objects.filter(agency=request.user)
    agent_activities = Activity.objects.filter(agency=request.user)

    # Calculate the bookings and revenue for each type of product
    flights_data = []
    for flight in agent_flights:
        bookings = Booking.objects.filter(custom_package__flights=flight)
        booking_count = bookings.count()
        revenue = sum(b.custom_package.get_total_price() for b in bookings)
        total_revenue += revenue
        monthly_bookings = bookings.filter(date_created__month=current_month)
        monthly_revenue += sum(booking.custom_package.get_total_price() for booking in monthly_bookings)

        flights_data.append({
            'flight': flight,
            'booking_count': booking_count,
            'revenue': revenue
        })

    hotels_data = []
    for hotel in agent_hotels:
        bookings = Booking.objects.filter(custom_package__hotels=hotel)
        booking_count = bookings.count()
        revenue = sum(b.custom_package.get_total_price() for b in bookings)
        total_revenue += revenue
        monthly_bookings = bookings.filter(date_created__month=current_month)

        hotels_data.append({
            'hotel': hotel,
            'booking_count': booking_count,
            'revenue': revenue
        })

    activities_data = []
    for activity in agent_activities:
        bookings = Booking.objects.filter(custom_package__activities=activity)
        booking_count = bookings.count()
        revenue = sum(b.custom_package.get_total_price() for b in bookings)
        total_revenue += revenue

        total_revenue += revenue
        monthly_bookings = bookings.filter(date_created__month=current_month)
        activities_data.append({
            'activity': activity,
            'booking_count': booking_count,
            'revenue': revenue
        })


    context = {
    'package_data': package_data,
    'flights_data': flights_data, 
    'hotels_data': hotels_data,
    'activities_data': activities_data,
    'total_revenue': total_revenue,
    'monthly_revenue': monthly_revenue,
    }

    return render(request, 'accounts/agent_dashboard.html', context)


@login_required
@user_passes_test(is_agent)
def flight_booking_detail(request, flight_id):
    # Find CustomPackages that include the specific flight
    custom_packages = CustomPackage.objects.filter(flights__id=flight_id)
    
    # Find bookings for these CustomPackages
    bookings = Booking.objects.filter(custom_package__in=custom_packages).distinct()
    booking_details = [{
        'username': booking.user.username,
        'first_name': booking.user.first_name,
        'last_name': booking.user.last_name,
        'email': booking.user.email,
        'user_id': booking.user.id,  # Make sure to include this line

    } for booking in bookings]

    return render(request, 'accounts/booking_detail.html', {'booking_details': booking_details})


@login_required
@user_passes_test(is_agent)
def hotel_booking_detail(request, hotel_id):
    # Find CustomPackages that include the specific hotel
    custom_packages = CustomPackage.objects.filter(hotels__id=hotel_id)
    
    # Find bookings for these CustomPackages
    bookings = Booking.objects.filter(custom_package__in=custom_packages).distinct()
    booking_details = [{
        'username': booking.user.username,
        'first_name': booking.user.first_name,
        'last_name': booking.user.last_name,
        'email': booking.user.email,
        'user_id': booking.user.id,  # Make sure to include this line

    } for booking in bookings]

    return render(request, 'accounts/booking_detail.html', {'booking_details': booking_details})

@login_required
@user_passes_test(is_agent)
def activity_booking_detail(request, activity_id):
    # Find CustomPackages that include the specific activity
    custom_packages = CustomPackage.objects.filter(activities__id=activity_id)
    
    # Find bookings for these CustomPackages
    bookings = Booking.objects.filter(custom_package__in=custom_packages).distinct()
    booking_details = [{
        'username': booking.user.username,
        'first_name': booking.user.first_name,
        'last_name': booking.user.last_name,
        'email': booking.user.email,
        'user_id': booking.user.id,  # Make sure to include this line

    } for booking in bookings]

    return render(request, 'accounts/booking_detail.html', {'booking_details': booking_details})

@login_required
@user_passes_test(is_agent)
def premade_package_booking_detail(request, package_id):
    # Get the premade package for the current agent
    try:
        premade_package = PreMadePackage.objects.get(id=package_id, agency=request.user)
    except PreMadePackage.DoesNotExist:
        messages.error(request, "Premade package not found.")
        return redirect('agent_dashboard')

    # Collect the bookings for the flights, hotels, and activities in the premade package
    bookings = Booking.objects.filter(
        Q(custom_package__flights__in=premade_package.flights.all()) | 
        Q(custom_package__hotels__in=premade_package.hotels.all()) | 
        Q(custom_package__activities__in=premade_package.activities.all()),
        custom_package__agency=request.user
    ).distinct()

    # Create a list of user details from the bookings
    booking_details = [{
        'username': booking.user.username,
        'first_name': booking.user.first_name,
        'last_name': booking.user.last_name,
        'email': booking.user.email,
        'user_id': booking.user.id,  # Make sure to include this line

    } for booking in bookings]

    return render(request, 'accounts/booking_detail.html', {'booking_details': booking_details})


@login_required
@user_passes_test(is_agent)
def send_notification(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        message = request.POST.get('message', 'Default notification message.')

        # Send the notification
        notify.send(request.user, recipient=user, verb='Notification', description=message)

        messages.success(request, f'Notification sent to {user.username}.')
        return redirect('agent_dashboard')  # Adjust as necessary
    else:
        messages.error(request, 'You can only send notifications with a POST request.')
        return redirect('agent_dashboard')  # Adjust as necessary
    

@login_required
def fetch_notifications(request):
    notifications = request.user.notifications.unread()
    return render(request, 'accounts/_notifications.html', {'notifications': notifications})

@login_required
def mark_notifications_as_read(request):
    request.user.notifications.mark_all_as_read()
    return JsonResponse({'status': 'success'})



@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        updated_question_text = request.POST.get('updated_question_text')
        question.question_text = updated_question_text
        question.save()
        return redirect('dashboard')  # Redirect to the dashboard after updating the question
    else:
        return redirect('dashboard')  # Redirect to the dashboard if the request method is not POST

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.delete()
    return redirect('dashboard')