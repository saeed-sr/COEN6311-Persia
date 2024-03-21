from django.db import models
from django.contrib.auth.models import User
from packages.models import CustomPackage
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('none', 'None'),
        ('reserved', 'Reserved'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_package = models.ForeignKey(CustomPackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='none')
    reserved_until = models.DateTimeField(null=True, blank=True)  # Add this field to track reservation expiration

    def __str__(self):
        return f"{self.user.username}'s booking for package {self.custom_package.id} - Status: {self.get_status_display()}"

    def is_reservation_expired(self):
        return timezone.now() > self.reserved_until if self.reserved_until else False
