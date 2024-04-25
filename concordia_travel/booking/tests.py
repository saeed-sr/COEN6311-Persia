from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Booking
from packages.models import CustomPackage
from django.utils import timezone
import datetime


class TestCompleteBooking(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client.login(username='testuser', password='password')
        self.custom_package = CustomPackage.objects.create(user=self.user)
        self.booking = Booking.objects.create(user=self.user, custom_package=self.custom_package)

    def test_complete_booking(self):
        response = self.client.post(reverse('complete_booking', args=[self.custom_package.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('booking_detail', args=[self.booking.id]))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'reserved')

