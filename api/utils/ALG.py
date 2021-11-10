from api.models import Operation
from api.models import Operation_type
from rest_framework.request import Request

class Operacja:
    def __init__(self, czas_rozpoczecia, czy_dziecko, czy_trudne):
        czas_rozpoczecia = self.czas_rozpoczecia
        czy_dziecko = self.czy_dziecko
        czy_trudne = self.czy_trudne

    def score:
        # punktacja dziecieca, punktacja doroslego, punktacja za trudnosc
        # TODO: poprawic punktowanie dla osoby doroslej
        return (czas_zakonczenia_pracy - czas_rozpoczecia)*czy_dziecko + (czas_zakonczenia_pracy - czas_rozpoczecia) + (czas_rozpoczecia - czas_rozpoczecia_pracy)*czy_trudne

    # TODO: test option when self == other (now: ret other. test: ret self)
    def __cmp__(self, other):
        if self.score > other.score:
            return self
        else:
            return other


def gatherDataFromDB(day_date, type_ICD):
    daily_operations = Operation.objects.raw("SELECT * FROM api_operation WHERE date = %s", [day_date])
    operation_type = Operation_type.objects.get(ICD_code=type_ICD)
    return daily_operations, operation_type

def sortListBasedOnRooms(daily_operations):
    """

    Args:
        daily_operations: QuerySet with all operations in defined day

    Returns: List with operations sorted based on room they are expected to be

    """
    # TEMP NOTE
    # How it is supposed to work
    # 1. take first room's number on list
    # 2. iterate through list and move operations of the same room to temp_list
    # 3. append temp_list to result a nd repeat the process until run out of rooms

    room_operation_list = []
    daily_operations_list = list(daily_operations)

    while daily_operations_list:
        temp_list = []
        room = daily_operations_list[0].room.room_number
        for operation in daily_operations_list:
            if operation.room.room_number == room:
                temp_list.append(operation)
                daily_operations_list.remove(operation)
        room_operation_list.append(temp_list)

    return room_operation_list


def processData(operacje_dnia, lekarz_ID, czy_dziecko, czy_trudne, czas_trwania, czas_przygotowania):
    """

    Args:
        operacje_dnia - lista list operacji, sortowane wedlug sal
        lekarz_ID - id lekarza w DB
        czy_trudne - wartosc -1/1
        czy_dziecko - wartosc -1/1
        czas_trwania - czas trwania operacji podany w minutch
        czas_przerwy - czas trwania przerwy pooperacyjnej podany w minutch

    Returns: Zwraca posortowana liste mozliwych operacji wedlug systemu okreslania zdatnosci

    """

    # Mozliwe pozycje dla operacji
    mozliwosci = []

    for operacje_w_jednej_sali in enumerate(operacje_dnia):
        for i,operacja in enumerate(operacje_w_jednej_sali):

            # Sprawdzanie przerw miedzy operacjami
            if i+1 < len(operacje_dnia):
                # Sprawdz przerwe miedzy i-ta operacja a i+1
                przerwa = operacja[rozpoczecie]+czas_trwania - operacje_w_jednej_sali[i+1][rozpoczecie]
                # Sprawdz czy mozna ustawic operacje w tej przerwie
                if przerwa + czas_przygotowania > czas_trwania:
                    # TAK: dodaj operacje do mozliwosci
                    mozliwosci.append(Operacja(czas_rozpoczecia, czy_dziecko, czy_trudne))

    # Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie
    # TODO: poprawic sprawdzanie przy operacjach dnia
    for operacja in operacje_dnia:
        for i,mozliwosc in enumerate(mozliwosci):
            if mozliwosc[godzina] == operacja[godzina]:
                if mozliwosc[lekarz] == operacja[lekarz]:
                    del(mozliwosci[i])

    # Posortuj liste mozliwosci za pomoca wyniku operacji
    mozliwosci.sort()

    return mozliwosci



def podpowiadanie_operacji():
    # Data from REST
    is_child = Request.POST["is_child"]
    day_date = Request.POST["date"]
    type_ICD = Request.POST["type_id"]

    # Data from Django about ward
    operation_prepare_time =
    working_start_houre =
    working_end_houre =
    enfding_houre_of_child_interval =
    begining_houre_of_difficult_interval =

    # Gather data from DB
    (daily_operations, operation_type) = gatherDataFromDB(day_date, type_ICD)

    # Prepare data for algorithm
    room_sorted_list = sortListBasedOnRooms(daily_operations)

    # Process data with algorithm
    sorted_possibilities = processData()

    # Prepare JSON out of possibilities
    return 1
