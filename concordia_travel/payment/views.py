
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, booking_id):
    if request.method == 'POST':
        # Create a Stripe PaymentIntent instead of directly charging the card
        # This is the recommended approach for handling payments now
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,  # Amount in cents. This should be dynamic based on the booking
                currency="usd",
                metadata={'integration_check': 'accept_a_payment', 'booking_id': booking_id},
            )
            # Send the client secret to the client to confirm the payment on the frontend
            return render(request, 'payment_success.html', {'client_secret': payment_intent.client_secret})
        except Exception as e:
            print(e)
            # Handle the exception

    else:
        context = {
            'stripe_key': settings.STRIPE_PUBLIC_KEY,
            'booking_id': booking_id
        }
        return render(request, 'payment/checkout.html', context)

def payment_success(request):
    # View to handle successful payment
    return render(request, 'payment_success.html')

def payment(request, booking_id):
    # Add your payment logic here
    pass