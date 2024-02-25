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
