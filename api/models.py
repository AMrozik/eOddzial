from django.db import models
from datetime import date
from .utils.pesel import Pesel


class PatientModel(models.Model):
    name = models.CharField(max_length=200, null=False)
    PESEL = models.CharField(max_length=12, null=False)

    def __eq__(self, other):
        if not isinstance(other, PatientModel):
            return NotImplemented
        return self.name == other.name and self.PESEL == other.PESEL

    @property
    def gender(self) -> str:
        p = Pesel(str(self.PESEL))
        return p.gender

    @property
    def age(self) -> int:
        p = Pesel(str(self.PESEL))
        return p.age(date.today())