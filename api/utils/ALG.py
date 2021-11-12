from api.models import Operation
from api.models import Operation_type
from api.models import Medic
from api.models import WardData
from rest_framework.request import Request

# class Operacja:
#     def __init__(self, czas_rozpoczecia, czy_dziecko, czy_trudne, medic):
#         czas_rozpoczecia = self.czas_rozpoczecia
#         czy_dziecko = self.czy_dziecko
#         czy_trudne = self.czy_trudne
#         self.medic = medic
#
#     def score(self):
#         # punktacja dziecieca, punktacja doroslego, punktacja za trudnosc
#         # TODO: poprawic punktowanie dla osoby doroslej
#         # return (czas_zakonczenia_pracy - czas_rozpoczecia)*czy_dziecko + (czas_zakonczenia_pracy - czas_rozpoczecia) + (czas_rozpoczecia - czas_rozpoczecia_pracy)*czy_trudne
#
#     # TODO: test option when self == other (now: ret other. test: ret self)
#     def __cmp__(self, other):
#         if self.score > other.score:
#             return self
#         else:
#             return other


class DailyHintALG:
    def __init__(self, is_child, day_date, type_ICD):
        # Data from REST
        self.is_child = is_child
        self.day_date = day_date
        self.type_ICD = type_ICD
        # self.medic_id = medic_id

        # Data about ward
        ward_data = WardData.objects.all()[0]
        operation_prepare_time = ward_data.operation_prepare_time
        working_start_hour = ward_data.working_start_hour
        working_end_hour = ward_data.working_end_hour
        child_interval_hour = ward_data.child_interval_hour
        difficult_interval_hour = ward_data.difficult_interval_hour

    def gatherDataFromDB(self):
        daily_operations = Operation.objects.raw("SELECT * FROM api_operation WHERE date = %s", [self.day_date])
        operation_type = Operation_type.objects.get(ICD_code=self.type_ICD)
        # medic = Medic.objects.get(name=medic_id)
        return daily_operations, operation_type

    def sortListBasedOnRooms(self, daily_operations):
        """

        Args:
            daily_operations: QuerySet with all operations in defined day

        Returns: List with operations sorted based on room they are expected to be

        """
        # DEV NOTE
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

    # def processData(room_sorted_list, lekarz_ID, czy_dziecko, czy_trudne, czas_trwania, czas_przygotowania):
    #
    #     # Mozliwe pozycje dla operacji
    #     mozliwosci = []
    #
    #     for operacje_w_jednej_sali in enumerate(room_sorted_list):
    #         for i,operacja in enumerate(operacje_w_jednej_sali):
    #
    #             # Sprawdzanie przerw miedzy operacjami
    #             if i+1 < len(room_sorted_list):
    #                 # Sprawdz przerwe miedzy i-ta operacja a i+1
    #                 przerwa = operacja[rozpoczecie]+czas_trwania - operacje_w_jednej_sali[i+1][rozpoczecie]
    #                 # Sprawdz czy mozna ustawic operacje w tej przerwie
    #                 if przerwa + czas_przygotowania > czas_trwania:
    #                     # TAK: dodaj operacje do mozliwosci
    #                     mozliwosci.append(Operacja(czas_rozpoczecia, czy_dziecko, czy_trudne))
    #
    #     # Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie
    #     # TODO: poprawic sprawdzanie przy operacjach dnia
    #     for operacja in operacje_dnia:
    #         for i,mozliwosc in enumerate(mozliwosci):
    #             if mozliwosc[godzina] == operacja[godzina]:
    #                 if mozliwosc[lekarz] == operacja[lekarz]:
    #                     del(mozliwosci[i])
    #
    #     # Posortuj liste mozliwosci za pomoca wyniku operacji
    #     mozliwosci.sort()
    #
    #     return mozliwosci

    def toJson(self):
        # Gather data from DB
        (daily_operations, operation_type) = self.gatherDataFromDB()

        # Prepare data for algorithm
        room_sorted_list = self.sortListBasedOnRooms(daily_operations)

        # Process data with algorithm
        # sorted_possibilities = processData()

        # Prepare JSON out of possibilities
        return 0
