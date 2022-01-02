from django.contrib import admin
from api.models import Patient, Medic, Operation, Operation_type, Room, WardData, NonAvailabilityRoom

# Register your models here.
admin.site.register(Patient)
admin.site.register(Operation)
admin.site.register(Operation_type)
admin.site.register(Medic)
admin.site.register(Room)
admin.site.register(WardData)
admin.site.register(NonAvailabilityRoom)

