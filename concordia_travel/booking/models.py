# booking/models.py
from django.db import models
from django.contrib.auth.models import User
from packages.models import CustomPackage

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_package = models.ForeignKey(CustomPackage, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)  # Indicates if the booking has been paid

    # Add other fields related to booking

    def __str__(self):
        return f"{self.user.username} - {self.custom_package.title}"
