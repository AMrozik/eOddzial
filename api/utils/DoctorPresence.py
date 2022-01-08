import datetime
from json import dumps, loads, JSONEncoder
from api.models import Medic, NonAvailabilityMedic


def checkPresence(day, medic_id):
    medic = Medic.objects.get(id=medic_id)
    absences = NonAvailabilityMedic.objects.filter(medic=medic)

    for absence in absences:
        if absence.date_start.date() <= day <= absence.date_end.date():
            return True
    return False
