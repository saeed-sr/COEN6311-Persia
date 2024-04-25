from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    agency = models.ForeignKey(User, related_name='flights_agent', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.airline} - {self.flight_number} ({self.departure_city} to {self.arrival_city})"

    # Add more fields as necessary

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Allows for an optional description
    agency = models.ForeignKey(User, related_name='hotels_agent', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.name} in {self.city}"

    # Add more fields as necessary

class Activity(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # E.g., sightseeing, hiking, etc.
    start_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Allows for an optional description
    agency = models.ForeignKey(User, related_name='activitys_agent', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.name} - {self.location}"
    # Add more fields as necessary


class CustomPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flights = models.ManyToManyField(Flight, blank=True)
    hotels = models.ManyToManyField(Hotel, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    is_booked = models.BooleanField(default=False)
    agency = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agency_custompackages')


    def __str__(self):
        if self.agency is None:
            user_info = f"{self.user.username}'s Custom Package:"

            flights_info = "Flights: " + ", ".join(str(flight) for flight in self.flights.all()) if self.flights.exists() else "No flights"
            hotels_info = "Hotels: " + ", ".join(str(hotel) for hotel in self.hotels.all()) if self.hotels.exists() else "No hotels"
            activities_info = "Activities: " + ", ".join(str(activity) for activity in self.activities.all()) if self.activities.exists() else "No activities"

            return f"{user_info}\n{flights_info}\n{hotels_info}\n{activities_info}"
        else:
            agency_info = "Agent: " f"{self.agency.username}"
            user_info = f"{self.user.username}'s Custom Package:"


            flights_info = "Flights: " + ", ".join(str(flight) for flight in self.flights.all()) if self.flights.exists() else "No flights"
            hotels_info = "Hotels: " + ", ".join(str(hotel) for hotel in self.hotels.all()) if self.hotels.exists() else "No hotels"
            activities_info = "Activities: " + ", ".join(str(activity) for activity in self.activities.all()) if self.activities.exists() else "No activities"

            return f"{user_info}\n{agency_info}\n{flights_info}\n{hotels_info}\n{activities_info}"
    
    def get_total_price(self):
        total_price = 0
        total_price += sum(flight.price for flight in self.flights.all())
        total_price += sum(hotel.price for hotel in self.hotels.all())
        total_price += sum(activity.price for activity in self.activities.all())
        return total_price
    

    

class AgentManager(models.Manager):
    def get_queryset(self):
        # Only return PreMadePackages created by users in the "agents" group
        agent_group = Group.objects.get(name='agents')
        return super().get_queryset().filter(agency__groups=agent_group)

class PreMadePackage(models.Model):
    agency = models.ForeignKey(User, on_delete=models.CASCADE)
    flights = models.ManyToManyField(Flight, blank=True)
    hotels = models.ManyToManyField(Hotel, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)

    objects = AgentManager()  # Use the custom manager

    def __str__(self):
        agency_info = f"{self.agency.username}'s Pre Made Package:"

        flights_info = "Flights: " + ", ".join(str(flight) for flight in self.flights.all()) if self.flights.exists() else "No flights"
        hotels_info = "Hotels: " + ", ".join(str(hotel) for hotel in self.hotels.all()) if self.hotels.exists() else "No hotels"
        activities_info = "Activities: " + ", ".join(str(activity) for activity in self.activities.all()) if self.activities.exists() else "No activities"

        return f"{agency_info}\n{flights_info}\n{hotels_info}\n{activities_info}"
    
    @property
    def name(self):
        # You can customize how you want to generate the name based on flights, hotels, and activities
        return f"Package for {self.agency.username}"

    @property
    def description(self):
        agency_info = f"Created by {self.agency.username}\n"

        flights_info = "Flights: " + ", ".join(str(flight) for flight in self.flights.all()) + "\n" if self.flights.exists() else ""
        hotels_info = "Hotels: " + ", ".join(str(hotel) for hotel in self.hotels.all()) + "\n" if self.hotels.exists() else ""
        activities_info = "Activities: " + ", ".join(str(activity) for activity in self.activities.all()) + "\n" if self.activities.exists() else ""

        package_info = "\n".join(filter(None, [agency_info, flights_info, hotels_info, activities_info]))

        return f"{package_info}"

    @property
    def calculate_total_price(self):
        # Calculate total price based on the associated flights, hotels, and activities
        flights_price = sum(flight.price for flight in self.flights.all())
        hotels_price = sum(hotel.price for hotel in self.hotels.all())
        activities_price = sum(activity.price for activity in self.activities.all())

        total_price = flights_price + hotels_price + activities_price
        print('test')

        return total_price


class CommentFlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.flight.flight_number} at {self.created_at}"

class CommentHotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.hotel.name} at {self.created_at}"
    
class CommentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.activity.name} at {self.created_at}"
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asked_questions')
    pre_made_package = models.ForeignKey(PreMadePackage, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answer_text = models.TextField(default='Not answered yet')
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Question from {self.user.username}"
    

