from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Building)
admin.site.register(Property)
admin.site.register(BuildingUnit)
admin.site.register(Room)
admin.site.register(EnergyMeter)