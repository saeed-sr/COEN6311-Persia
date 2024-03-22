
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from booking.models import Booking

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
import stripe

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    # Calculate the total amount to charge (in cents)
    total_amount = int(booking.custom_package.get_total_price() * 100)  # Convert to cents

    if request.method == 'POST':
        try:
            # Create a Stripe PaymentIntent with the dynamic amount
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency="usd",
                metadata={
                    'integration_check': 'accept_a_payment',
                    'booking_id': booking_id
                },
            )
            # If creation is successful, send client secret to the frontend
            return render(request, 'payment_success.html', {'client_secret': payment_intent.client_secret})
        except Exception as e:
            # Print the exception for debugging
            print(e)
            # Add more robust error handling here
            context = {
                'error_message': "An error occurred while trying to process your payment. Please try again.",
                'stripe_key': settings.STRIPE_PUBLIC_KEY,
                'booking': booking
            }
            return render(request, 'payment/checkout.html', context)

    else:
        # For GET request, pass the booking and stripe key to the template
        context = {
            'stripe_key': settings.STRIPE_PUBLIC_KEY,
            'booking': booking
        }
        return render(request, 'payment/checkout.html', context)


@login_required
def payment_success(request, booking_id):
    # Get the booking object
    booking = get_object_or_404(Booking, pk=booking_id)

    # Update the status to 'paid' or 'complete'
    booking.status = 'paid'  # or 'complete', depending on your STATUS_CHOICES in the Booking model
    booking.save()

    # Render the payment success template
    return render(request, 'payment/payment_success.html', {'booking': booking})


def payment(request, booking_id):
    # Add your payment logic here
    pass