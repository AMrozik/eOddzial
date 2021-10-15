import datetime
import re


class Pesel:
    def __init__(self, pesel: str):
        if not _proper_format(pesel):
            raise MalformedPesel()
        if not pesel.endswith(_control_digit(pesel)):
            raise InvalidPesel("Mismatched control digit")
        if not _valid_birth_month(pesel):
            raise InvalidPesel("Month not in range")
        if not _valid_birth_day(pesel):
            raise InvalidPesel("Day not in range")
        self.pesel = pesel

    @property
    def gender(self) -> str:
        return 'female' if self._is_female() else 'male'

    def _is_female(self):
        return int(self.pesel[-2]) % 2 == 0

    @property
    def year(self) -> int:
        month = int(self.pesel[2:4])

        if 0 < month < 13:
            year = 1900
        elif 20 < month < 33:
            year = 2000
        elif 40 < month < 53:
            year = 2100
        elif 60 < month < 73:
            year = 2200
        elif 80 < month < 93:
            year = 1800
        else:
            year = 0

        return year + int(self.pesel[0:2])

    @property
    def month(self) -> int:
        pesel_month = int(self.pesel[2:4])

        if 0 < pesel_month < 13:
            return pesel_month
        elif 20 < pesel_month < 33:
            pesel_month -= 20
        elif 40 < pesel_month < 53:
            pesel_month -= 40
        elif 60 < pesel_month < 73:
            pesel_month -= 60
        elif 80 < pesel_month < 93:
            pesel_month -= 80

        return pesel_month

    @property
    def day(self) -> int:
        return int(self.pesel[4:6])

    def age(self, _date: datetime.date) -> int:
        if _date.month > self.month:
            return _date.year - self.year
        elif _date.month == self.month and _date.day >= self.day:
            return _date.year - self.year
        else:
            return _date.year - self.year - 1

    def __str__(self):
        return self.pesel

    def __eq__(self, other):
        if not isinstance(other, Pesel):
            return NotImplemented
        return self.pesel == other.pesel


def _proper_format(pesel: str) -> bool:
    return bool(re.match(r"^[0-9]{11}$", pesel))


def _control_digit(pesel: str) -> str:
    _sum = 0
    for digit, wage in zip(pesel, [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]):
        _sum += int(digit) * wage
    return str((10 - _sum % 10) % 10)


def _valid_birth_day(pesel: str) -> bool:
    day = int(pesel[4:6])

    return 1 <= day <= 31


def _valid_birth_month(pesel: str) -> bool:
    pesel_month = int(pesel[2:4])

    return 1 <= (pesel_month % 20) <= 12


class MalformedPesel(Exception):
    pass


class InvalidPesel(Exception):
    pass
