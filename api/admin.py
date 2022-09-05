from django.contrib import admin

from api.models import Patient, Medic, Operation, OperationType, Room, WardData, NonAvailabilityRoom, NonAvailabilityMedic, BudgetYear, Log

admin.site.register(Patient)
admin.site.register(Operation)
admin.site.register(OperationType)
admin.site.register(Medic)
admin.site.register(Room)
admin.site.register(WardData)
admin.site.register(NonAvailabilityRoom)
admin.site.register(Log)
admin.site.register(NonAvailabilityMedic)
admin.site.register(BudgetYear)

