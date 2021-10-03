from django.db import models
from datetime import date


class Patient(models.Model):
    name = models.CharField(max_length=200, null=False)
    pesel = models.CharField(max_length=12, null=False)

    # @property
    # def gender(self) -> str:
    #     _pesel = pesel.Pesel(str(self.pesel))
    #     return _pesel.gender

    # seems redundant to me
    # @property
    # def id(self):
    #     return str(self.pesel)

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self.name == other.name and self.pesel == other.pesel

    # def age(self, _date: date) -> int:
    #     _pesel = pesel.Pesel(str(self.pesel))
    #     return _pesel.age(_date)
