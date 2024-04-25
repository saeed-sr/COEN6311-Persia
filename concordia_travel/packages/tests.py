from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Flight, CustomPackage
from booking.models import Booking
from unittest.mock import patch
import datetime
from django.utils import timezone


class PackageBookingTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        
        # Create a flight
        self.flight = Flight.objects.create(
            flight_number="AB123",
            airline="TestAir",
            departure_city="CityA",
            arrival_city="CityB",
            departure_time=timezone.now() + datetime.timedelta(days=1),
            duration=datetime.timedelta(hours=2),
            price=200.00
        )

    def test_book_flight(self):
        # Check initial count of bookings
        initial_count = Booking.objects.count()
        
        # Perform the booking
        response = self.client.post(reverse('book_flight', args=[self.flight.id]))
        
        # Check the response
        self.assertEqual(response.status_code, 302)  # Redirect to flight detail page
        self.assertEqual(Booking.objects.count(), initial_count + 1)  # Ensure a booking was added
        self.assertTrue(Booking.objects.filter(user=self.user, custom_package__flights__in=[self.flight]).exists())
        self.assertRedirects(response, reverse('flight_detail', args=[self.flight.id]))

    def test_book_flight_not_logged_in(self):
        # Ensure no user is logged in
        self.client.logout()
        
        # Try to book a flight while not logged in
        response = self.client.post(reverse('book_flight', args=[self.flight.id]), follow=True)
        
        # Check the response to see if it redirects to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('book_flight', args=[self.flight.id])}")
        # Ensure no booking was made
        self.assertFalse(Booking.objects.exists())



class FlightManagementTests(TestCase):

    def setUp(self):
        # Create an agent user
        self.agent_user = User.objects.create_user(username='agentuser', password='secret')
        self.agent_group = Group.objects.create(name='agents')
        self.agent_group.user_set.add(self.agent_user)
        self.client.login(username='agentuser', password='secret')

        # Create a form data sample
        self.flight_data = {
            'flight_number': 'AB456',
            'airline': 'FlyHigh',
            'departure_city': 'CityX',
            'arrival_city': 'CityY',
            'departure_time': timezone.now() + datetime.timedelta(days=2),
            'duration': datetime.timedelta(hours=5),
            'price': 300.00
        }

    @patch('django.contrib.auth.decorators.user_passes_test')
    def test_add_flight(self, mock_user_passes_test):
        mock_user_passes_test.return_value = True  # Assume the user passes the test
        
        # Post data to create a flight
        response = self.client.post(reverse('add_flight'), self.flight_data, follow=True)
        
        # Verify flight was created and redirect occurred
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Flight.objects.filter(flight_number='AB456').exists())
        self.assertEqual(Flight.objects.last().agency, self.agent_user)  # Ensure the agency is assigned correctly
        self.assertContains(response, 'Flight added successfully!')

    def test_add_flight_with_incomplete_data(self):
        # Incomplete flight data (missing required fields)
        incomplete_flight_data = {
            'flight_number': 'AB456',
            'airline': '',  # Empty string for a required field
            'departure_city': 'CityX',
            'arrival_city': '',
            'departure_time': timezone.now() + datetime.timedelta(days=2),
            'duration': datetime.timedelta(hours=5),
            'price': 300.00
        }

        response = self.client.post(reverse('add_flight'), incomplete_flight_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Flight.objects.filter(flight_number='AB456').exists())

        # Access form from response context
        if 'form' in response.context:
            form = response.context['form']
            # Check for specific field errors
            self.assertTrue(form.errors['airline'], ['This field is required.'])
            self.assertTrue(form.errors['arrival_city'], ['This field is required.'])
        else:
            self.fail("No form in context")
