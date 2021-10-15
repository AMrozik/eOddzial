from datetime import date
from .pesel import Pesel


class Patient:
    def __init__(self, name: str, pesel: Pesel):
        if name == '':
            raise ValueError('Empty patient name')
        self.name = name
        self.pesel = pesel

    @property
    def gender(self) -> str:
        return self.pesel.gender

    @property
    def id(self):
        return str(self.pesel)

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self.name == other.name and \
            self.pesel == other.pesel

    def age(self, _date: date) -> int:
        return self.pesel.age(_date)
