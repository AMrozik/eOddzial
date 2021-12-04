from django.db import models
from datetime import date
from .utils.pesel import Pesel
import re


def code(icd: str) -> bool:
    return bool(re.match(r"^[0-9]{2,3}(\.[0-9]{1,5})?$", icd))


class Patient(models.Model):
    name = models.CharField(max_length=200, null=False)
    PESEL = models.CharField(max_length=12, null=False)

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self.name == other.name and self.PESEL == other.PESEL

    def __hash__(self):
        return super().__hash__()

    @property
    def gender(self) -> str:
        p = Pesel(str(self.PESEL))
        return p.gender

    @property
    def age(self) -> int:
        p = Pesel(str(self.PESEL))
        return p.age(date.today())


# class Day(models.Model):
#     year = models.IntegerField(null=False)
#     month = models.IntegerField(null=False)
#     day = models.IntegerField(null=False)


class Medic(models.Model):
    name = models.CharField(max_length=200, null=False)


class Operation_type(models.Model):
    name = models.CharField(max_length=200, null=False)
    ICD_code = models.CharField(max_length=200, null=False)
    cost = models.IntegerField(null=False)
    is_difficult = models.BooleanField()
    duration = models.DurationField()

    def validate_icd_code(self):
        return code(str(self.ICD_code))


class NonAvailabilityMedic(models.Model):
    medic = models.ForeignKey('Medic', on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()


class Room(models.Model):
    room_number = models.IntegerField(null=False)


class NonAvailabilityRoom(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()


class Operation(models.Model):
    type = models.ForeignKey('Operation_type', on_delete=models.CASCADE)
    medic = models.ForeignKey('Medic', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateField(null=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    start = models.TimeField()


class WardData(models.Model):
    operation_prepare_time = models.TimeField()
    working_start_hour = models.TimeField()
    working_end_hour = models.TimeField()
    child_interval_hour = models.TimeField()
    difficult_interval_hour = models.TimeField()



