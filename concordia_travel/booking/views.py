from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CustomPackage
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from django.shortcuts import get_object_or_404

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
        return redirect('index')  # Adjust the URL name as needed

    except CustomPackage.DoesNotExist:
        messages.error(request, 'Invalid custom package ID')
        return redirect('error_page')  # Adjust the URL name for an error page


@login_required
def complete_booking(request, custom_package_id):
    # Ensure this is only accessed via POST
    if request.method == 'POST':
        custom_package = get_object_or_404(CustomPackage, pk=custom_package_id, user=request.user)
        booking, created = Booking.objects.get_or_create(
            user=request.user,
            custom_package=custom_package,
            defaults={'status': 'reserved', 'reserved_until': timezone.now() + timedelta(hours=1)}
        )

        # You might need to update the booking status here based on your logic
        # For now, assuming the booking gets 'reserved' status immediately
        booking.status = 'reserved'
        booking.save()

        messages.success(request, 'Booking is now reserved. Please complete the payment.')
        return redirect('booking_detail', booking_id=booking.id)
    else:
        return redirect('view_bookings')

@login_required
def view_bookings(request):
    # Retrieve bookings for the user that are not paid yet or are reserved
    current_bookings = Booking.objects.filter(
        user=request.user, 
        status__in=['none', 'reserved']
    ).exclude(
        reserved_until__lt=timezone.now()
    )
    old_bookings = Booking.objects.filter(user=request.user, status='paid')
    
    context = {
        'current_bookings': current_bookings,
        'old_bookings': old_bookings,
    }
    print(context)

    return render(request, 'booking/view_bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    # Pass the booking to the template
    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
@require_POST
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, status='none')
    custom_package = booking.custom_package
    booking.delete()
    custom_package.delete()  # Assuming you also want to delete the custom package when the booking is deleted.
    messages.info(request, 'Booking deleted successfully.')
    return redirect('view_bookings')


@login_required
def share_your_experience(request): 
    pass

