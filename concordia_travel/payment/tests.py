from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Booking, CustomPackage
from unittest.mock import patch
from booking.models import Booking

from django.conf import settings
from django.contrib.messages import get_messages
from django.contrib import messages



# Mock stripe.PaymentIntent.create to not actually call Stripe's API
@patch('stripe.PaymentIntent.create')
class PaymentTests(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client = Client()
        self.client.login(username='testuser', password='secret')

        # Create an agency user if required
        self.agency_user = User.objects.create_user(username='testagency', password='secret')
        
        # Create related objects if necessary
        # flight = Flight.objects.create(...)
        # hotel = Hotel.objects.create(...)
        # activity = Activity.objects.create(...)

        # Create the CustomPackage with the necessary relations
        self.custom_package = CustomPackage.objects.create(
            user=self.user,
            # Assuming the agency is optional, if not, assign it like: agency=self.agency_user
        )

        # Add relations if necessary
        # self.custom_package.flights.add(flight)
        # self.custom_package.hotels.add(hotel)
        # self.custom_package.activities.add(activity)
        
        # The total_price needs to be calculated based on related objects
        # Here we just mock the total price for the sake of the test
        total_price_mock = 100.0  # Replace with actual calculation if necessary

        self.booking = Booking.objects.create(
            user=self.user, 
            custom_package=self.custom_package,
            # Assuming you have a field for price in Booking or a method to calculate it
            # If the price is calculated based on the CustomPackage, mock the price
            # price=total_price_mock  # Replace with actual method call if necessary
        )


    def test_checkout_success(self, mock_create):
        # Configure the mock to return a successful response
        mock_create.return_value = {
            'id': 'fake-payment-intent-id',
            'client_secret': 'fake-client-secret'
        }
        
        # Send POST request to checkout
        response = self.client.post(reverse('checkout', args=[self.booking.id]), follow=True)
        
        # Check if the redirect was successful
        self.assertRedirects(response, reverse('payment_success', args=[self.booking.id]))
        # Check if the payment was marked successful
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'paid')


def test_checkout_error(self, mock_create):
    # Configure the mock to raise an exception
    mock_create.side_effect = Exception('Payment failed')
    
    # Send POST request to checkout
    response = self.client.post(reverse('checkout', args=[self.booking.id]), follow=True)
    
    # Ensure that messages were added to the context
    all_messages = [str(message) for message in messages.get_messages(response.wsgi_request)]
    
    # Check if any of the messages is an error message
    self.assertTrue(any("An error occurred while trying to process your payment" in message for message in all_messages), "Error message not found in response messages")
