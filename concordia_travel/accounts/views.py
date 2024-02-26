from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test


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


def user_dashboard(request):
    pass

@login_required
def user_dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
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
def add_flight(request):
    # ... add flight logic for agents
    pass

@login_required
@user_passes_test(is_agent)
def add_hotel(request):
    # ... add hotel logic for agents
    pass

@login_required
@user_passes_test(is_agent)
def add_activity(request):
    # ... add activity logic for agents
    pass