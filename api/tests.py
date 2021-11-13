import datetime
from unittest.mock import patch

from django.test import TestCase
from django.db.models import Count
from .utils.ALG import DailyHintALG, PossibleOperation
from .models import WardData, Operation, Operation_type, Medic, Patient, Room

# Create your tests here.


class DailyHintingTest(TestCase):
    def setUp(self):
        # DB
        WardData.objects.create(operation_prepare_time="0:15",
                                working_start_hour="8:00",
                                working_end_hour="16:00",
                                child_interval_hour="10:00",
                                difficult_interval_hour="15:00")

        Operation_type.objects.create(name="type1",
                                      ICD_code="12",
                                      cost=12000,
                                      is_difficult=True,
                                      duration="1:00")

        Operation_type.objects.create(name="type2",
                                      ICD_code="12b",
                                      cost=12001,
                                      is_difficult=False,
                                      duration="1:05")

        Medic.objects.create(name="Krzysztof",
                             work_start="8:00",
                             work_end="16:00")

        Patient.objects.create(name="Karol",
                               PESEL="98021400000")

        Room.objects.create(room_number=3)
        Room.objects.create(room_number=2)

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=2),
                                 start="12:00")

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12b"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=3),
                                 start="14:00")

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12b"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=2),
                                 start="15:00")

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12b"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=3),
                                 start="10:00")

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12b"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=2),
                                 start="9:00")

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12b"),
                                 medic=Medic.objects.get(name="Krzysztof"),
                                 patient=Patient.objects.get(name="Karol"),
                                 date="2021-10-10",
                                 room=Room.objects.get(room_number=3),
                                 start="9:00")

    def testWardDataMock(self):
        ward_data = WardData.objects.all()[0]
        self.assertEqual(ward_data.operation_prepare_time, datetime.time(0, 15))
        self.assertEqual(ward_data.working_start_hour, datetime.time(8, 0))
        self.assertEqual(ward_data.working_end_hour, datetime.time(16, 0))
        self.assertEqual(ward_data.child_interval_hour, datetime.time(10, 0))
        self.assertEqual(ward_data.difficult_interval_hour, datetime.time(15, 0))

    def testConstructingAlgObject(self):
        algorithm = DailyHintALG(True, "2021-10-10", "12b")
        self.assertTrue(algorithm.is_child)
        self.assertEqual(algorithm.day_date, "2021-10-10")
        self.assertEqual(algorithm.type_ICD, "12b")

    def testGatheringDataFromDB(self):
        algorithm = DailyHintALG(True, "2021-10-10", "12b")

        (daily_operations, operation_type) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date="2021-10-10"))

        self.assertTrue(len(daily_operations) == operations_amount)
        self.assertEqual(operation_type.name, "type2")

    def testGatheringDataFromDBDifferentDay(self):
        algorithm = DailyHintALG(True, "2021-10-11", "12b")

        (daily_operations, operation_type) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date="2021-10-11"))

        self.assertTrue(len(daily_operations) == operations_amount)
        self.assertEqual(operation_type.name, "type2")

    def testSortingByRoomsEquals(self):
        algorithm = DailyHintALG(True, "2021-10-10", "12b")
        (daily_operations, operation_type) = algorithm.gatherDataFromDB()

        sorted_list = algorithm.sortListBasedOnRooms(daily_operations)

        rooms = list(Operation.objects.values('room').annotate(dcount=Count('room')).order_by())
        rooms_amount = 0
        for e in rooms:
            rooms_amount += 1

        self.assertTrue(len(sorted_list) == rooms_amount)

    # Uncomment if you now how to properly mock PossibleOperation.score method
    # @patch('PossibleOperation.score')
    # def testPossibleOperationCMP(self, mock_score):
    #     # TODO: mock score() and test properly next time ;)
    #     test = PossibleOperation(12*(60*60), False, False, 2, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
    #     test2 = PossibleOperation(11*(60*60), False, False, 2, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
    #     test3 = PossibleOperation(11*(60*60), False, False, 2, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
    #
    #     mock_score.return_value = 3
    #
    #     self.assertTrue(test > test2)
    #     self.assertTrue(test >= test2)
    #     self.assertFalse(test < test2)
    #     self.assertFalse(test <= test2)
    #
    #     self.assertTrue(test3 >= test2)
    #     self.assertTrue(test3 <= test2)
    #     self.assertTrue(test3 == test2)
    #
    #     self.assertTrue(test != test2)

    def testPossibleOperationScoreIsChildInChildInterval(self):
        adult = PossibleOperation(9*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        child = PossibleOperation(9*(60*60), True, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(child > adult)

    def testPossibleOperationScoreIsChildOutChildInterval(self):
        adult = PossibleOperation(12*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        child = PossibleOperation(12*(60*60), True, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(child > adult)

    def testPossibleOperationScoreDifficultOutDifficultInterval(self):
        easy = PossibleOperation(9*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        difficult = PossibleOperation(9*(60*60), False, True, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(difficult < easy)

    def testPossibleOperationScoreDifficultInDifficultInterval(self):
        easy = PossibleOperation(16*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        difficult = PossibleOperation(16*(60*60), False, True, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(difficult > easy)

    def testPossibleOperationScoreNormalInChildInterval(self):
        earlier = PossibleOperation(8*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        later = PossibleOperation(9*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(earlier < later)

    def testPossibleOperationScoreNormalOutChildInterval(self):
        earlier = PossibleOperation(11*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))
        later = PossibleOperation(12*(60*60), False, False, 0, 8*(60*60), 16*(60*60), 10*(60*60), 15*(60*60))

        self.assertTrue(earlier > later)



