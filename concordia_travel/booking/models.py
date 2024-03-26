from django.db import models
from django.contrib.auth.models import User
from packages.models import CustomPackage
from django.utils import timezone
import uuid

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
    tracking_id = models.CharField(max_length=64, editable=False, null=True)

    def __str__(self):
        return f"{self.user.username}'s booking for package {self.custom_package.id} - Status: {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Only set the tracking_id if the booking is being created (and not on update)
        if not self.tracking_id:
            # This will generate a random UUID, you could use other methods if you prefer
            self.tracking_id = str(uuid.uuid4())
        super(Booking, self).save(*args, **kwargs)

    def is_reservation_expired(self):
        return timezone.now() > self.reserved_until if self.reserved_until else False
    
    def create_tracking_id(self):
        pass
