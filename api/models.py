from django.db import models
from datetime import date


class PatientModel(models.Model):
    name = models.CharField(max_length=200, null=False)
    pesel = models.CharField(max_length=12, null=False)
    gender = models.CharField(max_length=20, null=False)
    age = models.IntegerField()