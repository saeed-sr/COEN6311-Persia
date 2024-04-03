from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from packages.models import Question
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from packages.models import PreMadePackage
from booking.models import Booking
from django.db.models import Q

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
    return render(request, 'accounts/dashboard.html', {'user_questions': user_questions})

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
    # Get all premade packages created by the agent
    premade_packages = PreMadePackage.objects.filter(agency=request.user)

    # Calculate bookings and revenues
    package_data = []
    total_revenue = 0
    monthly_revenue = 0
    current_month = datetime.now().month

    for package in premade_packages:
        # Get all CustomPackage objects that include any of the flights, hotels, or activities of the current premade package
        bookings = Booking.objects.filter(
            Q(custom_package__flights__in=package.flights.all()) | 
            Q(custom_package__hotels__in=package.hotels.all()) | 
            Q(custom_package__activities__in=package.activities.all()), 
            custom_package__agency=request.user
        ).distinct()
        booking_count = bookings.count()
        revenue = sum(b.custom_package.get_total_price() for b in bookings)
        monthly_bookings = bookings.filter(date_created__month=current_month)
        monthly_revenue += sum(b.custom_package.get_total_price() for b in monthly_bookings)
        total_revenue += revenue

        package_data.append({
            'package': package,
            'booking_count': booking_count,
            'revenue': revenue
        })

    context = {
        'package_data': package_data,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, 'accounts/agent_dashboard.html', context)


