import django_tables2 as tables
from .models import Flight, Hotel, Activity

class FlightTable(tables.Table):
    details = tables.LinkColumn('hotel_detail', args=[tables.A('pk')], text='Details', verbose_name='Details', attrs={"class": "btn btn-primary btn-sm"})

    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'duration', 'price')
        template_name = "django_tables2/bootstrap4.html"

class HotelTable(tables.Table):
    details = tables.LinkColumn('hotel_detail', args=[tables.A('pk')], text='Details', verbose_name='Details', attrs={"class": "btn btn-primary btn-sm"})

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'city', 'phone_number', 'price')  # Remove 'description' from fields
        template_name = "django_tables2/bootstrap4.html"

class ActivityTable(tables.Table):
    details = tables.LinkColumn('hotel_detail', args=[tables.A('pk')], text='Details', verbose_name='Details', attrs={"class": "btn btn-primary btn-sm"})

    class Meta:
        model = Activity
        fields = ('id', 'name', 'location', 'type', 'start_time', 'duration', 'price')
        template_name = "django_tables2/bootstrap4.html"
