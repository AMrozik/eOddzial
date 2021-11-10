from django.contrib import admin
from api.models import Patient
from api.models import Operation
from api.models import Operation_type
from api.models import Medic
from api.models import Room

# Register your models here.
admin.site.register(Patient)
admin.site.register(Operation)
admin.site.register(Operation_type)
admin.site.register(Medic)
admin.site.register(Room)
