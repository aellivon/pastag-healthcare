# Core admin
from django.contrib import admin
from .models import BloodPressure, Weight, Height

admin.site.register(BloodPressure)
admin.site.register(Weight)
admin.site.register(Height)

