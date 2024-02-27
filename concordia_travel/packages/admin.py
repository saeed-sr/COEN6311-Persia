from django.contrib import admin
from .models import Flight, Hotel, Activity, CustomPackage, PreMadePackage

admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(Activity)
admin.site.register(CustomPackage)
admin.site.register(PreMadePackage)