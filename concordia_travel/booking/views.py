from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CustomPackage

@login_required
@require_POST
def book_custom_package(request):
    # Access data from the request body
    custom_package_id = request.POST.get('custom_package_id')

    try:
        custom_package = CustomPackage.objects.get(pk=custom_package_id)
        # Process your booking logic here

        # Redirect to homepage or another appropriate page
        messages.success(request, 'Booking successful!')
        return redirect('homepage')  # Adjust the URL name as needed

    except CustomPackage.DoesNotExist:
        messages.error(request, 'Invalid custom package ID')
        return redirect('error_page')  # Adjust the URL name for an error page


@login_required
def view_bookings(request):
    # Retrieve current custom packages for the user
    current_custom_packages = CustomPackage.objects.filter(user=request.user, is_booked=False)
    
    # Retrieve old bookings for the user
    old_bookings = CustomPackage.objects.filter(user=request.user, is_booked=True)
    
    context = {
        'current_custom_packages': current_custom_packages,
        'old_bookings': old_bookings,
    }
    
    return render(request, 'booking/view_bookings.html', context)


def complete_booking(request, custom_package_id):
    pass 