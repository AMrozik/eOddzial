import datetime
from unittest.mock import patch

from django.test import TestCase
from django.db.models import Count
from .utils.ALG import DailyHintALG, PossibleOperation, dateTimeToInt, intToDateTime
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

        Medic.objects.create(name="Oleg",
                             work_start="8:00",
                             work_end="16:00")

        Patient.objects.create(name="Karol",
                               PESEL="98021400000")

        Room.objects.create(room_number=3)
        Room.objects.create(room_number=2)
        Room.objects.create(room_number=16)

        Operation.objects.create(type=Operation_type.objects.get(ICD_code="12"),
                                 medic=Medic.objects.get(name="Oleg"),
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

    # -----------------------------------------------------------------------------------------------------------------
    # TESTING MOCKED DATA

    def testWardDataMock(self):
        ward_data = WardData.objects.all()[0]
        self.assertEqual(ward_data.operation_prepare_time, datetime.time(0, 15))
        self.assertEqual(ward_data.working_start_hour, datetime.time(8, 0))
        self.assertEqual(ward_data.working_end_hour, datetime.time(16, 0))
        self.assertEqual(ward_data.child_interval_hour, datetime.time(10, 0))
        self.assertEqual(ward_data.difficult_interval_hour, datetime.time(15, 0))

    def testConstructingAlgObject(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-10", "12b", medic_id)
        self.assertTrue(algorithm.is_child)
        self.assertEqual(algorithm.day_date, "2021-10-10")
        self.assertEqual(algorithm.type_ICD, "12b")

    # -----------------------------------------------------------------------------------------------------------------
    # GATHERING DATA FROM DB TESTS

    def testGatheringDataFromDB(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-10", "12b", medic_id)

        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date="2021-10-10"))
        self.assertTrue(len(daily_operations) == operations_amount)

        self.assertEqual(operation_type.name, "type2")

        self.assertTrue(medic.name == "Krzysztof")

        rooms_amount = len(Room.objects.all())
        self.assertTrue(len(rooms) == rooms_amount)

    def testGatheringDataFromDBDifferentDay(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-11", "12b", medic_id)

        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date="2021-10-11"))
        self.assertTrue(len(daily_operations) == operations_amount)

        self.assertEqual(operation_type.name, "type2")

        self.assertTrue(medic.name == "Krzysztof")

        rooms_amount = len(Room.objects.all())
        self.assertTrue(len(rooms) == rooms_amount)

    # -----------------------------------------------------------------------------------------------------------------
    # SORTING BY ROOMS TESTS

    def testSortingByRoomsEquals(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-10", "12b", medic_id)
        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()

        sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)

        rooms_in_ward = len(Room.objects.all())
        rooms_amount = 0
        for e in range(rooms_in_ward):
            rooms_amount += 1

        self.assertTrue(len(sorted_list) == rooms_amount)

    # -----------------------------------------------------------------------------------------------------------------
    # TIME CONVERSION

    def testDateTimeToInt(self):
        time = datetime.time(hour=16, minute=20, second=5)

        conversed = dateTimeToInt(time)

        self.assertTrue(conversed == 16*60*60 + 20*60 + 5)

    def testIntToDateTime(self):
        time = datetime.time(hour=16, minute=20, second=5)
        value = 16*60*60 + 20*60 + 5

        conversed = intToDateTime(value)

        self.assertTrue(conversed == time)

    # -----------------------------------------------------------------------------------------------------------------
    # POSSIBLE OPERATION SCORE TESTS

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
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=9, minute=0, second=0)

        adult = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(child > adult)

    def testPossibleOperationScoreIsChildOutChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=12, minute=0, second=0)

        adult = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(child > adult)

    def testPossibleOperationScoreDifficultOutDifficultInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=9, minute=0, second=0)

        easy = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        difficult = PossibleOperation(time_start, False, True, 0, False, time1, time2, time3, time4)

        self.assertTrue(difficult < easy)

    def testPossibleOperationScoreDifficultInDifficultInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=16, minute=0, second=0)

        easy = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        difficult = PossibleOperation(time_start, False, True, 0, False, time1, time2, time3, time4)

        self.assertTrue(difficult > easy)

    def testPossibleOperationScoreNormalInChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=8, minute=0, second=0)
        time_start2 = datetime.time(hour=9, minute=0, second=0)

        earlier = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        later = PossibleOperation(time_start2, False, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(earlier < later)

    def testPossibleOperationScoreNormalOutChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=11, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        earlier = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        later = PossibleOperation(time_start2, False, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(earlier > later)

    def testPossibleOperationScoreNormalInVsOutChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=9, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        earlier = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)
        later = PossibleOperation(time_start2, False, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(earlier < later)

    def testPossibleOperationScoreChildVsNormalInChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=9, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)
        adult = PossibleOperation(time_start2, False, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(child > adult)

    def testPossibleOperationScoreChildVsNormalOutChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=12, minute=0, second=0)

        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)
        adult = PossibleOperation(time_start, False, False, 0, False, time1, time2, time3, time4)

        self.assertTrue(child > adult)

    def testPossibleOperationScoreChildVsDifficultInChildInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=9, minute=0, second=0)

        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)
        difficult = PossibleOperation(time_start, False, True, 0, False, time1, time2, time3, time4)

        self.assertTrue(child > difficult)

    def testPossibleOperationScoreChildVsDifficultInDifficultInterval(self):
        time1 = datetime.time(hour=8, minute=0, second=0)
        time2 = datetime.time(hour=16, minute=0, second=0)
        time3 = datetime.time(hour=10, minute=0, second=0)
        time4 = datetime.time(hour=15, minute=0, second=0)

        time_start = datetime.time(hour=16, minute=0, second=0)

        child = PossibleOperation(time_start, True, False, 0, False, time1, time2, time3, time4)
        difficult = PossibleOperation(time_start, False, True, 0, False, time1, time2, time3, time4)

        self.assertTrue(child < difficult)

    # -----------------------------------------------------------------------------------------------------------------
    # PROCESS DATA TESTS

    # OBSOLETE
    # def testProcessDataRemovingCollidingWithExistingOperation(self):
    #     medic_id = Medic.objects.get(name="Krzysztof").id
    #     algorithm = DailyHintALG(True, True, "2021-10-11", "12b", medic_id)
    #     (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
    #     sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
    #
    #     possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)
    #
    #     is_colliding = False
    #     for room_operations in sorted_list:
    #         for operation in room_operations:
    #             for possibility in possibilities:
    #                 if dateTimeToInt(operation.start) <= possibility.start_hour <= dateTimeToInt(operation.start) + int(operation.type.duration.total_seconds()):
    #                     is_colliding = True
    #
    #     self.assertTrue(not is_colliding)

    # OBSOLETE
    # def testProcessDataRemovingCollidingWithMedicsOperations(self):
    #     medic_id = Medic.objects.get(name="Krzysztof").id
    #     algorithm = DailyHintALG(True, True, "2021-10-11", "12b", medic_id)
    #     (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
    #     sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
    #
    #     possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)
    #
    #     medic_operations = Operation.objects.filter(medic=medic)
    #     is_colliding = False
    #     for medic_operation in medic_operations:
    #         for possible_operation in possibilities:
    #             if dateTimeToInt(medic_operation.start) < possible_operation.start_hour < (dateTimeToInt(medic_operation.start) + int(medic_operation.type.duration.total_seconds())):
    #                 is_colliding = True
    #
    #     self.assertTrue(not is_colliding)

    def testProcessDataDayEmpty(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-11", "12b", medic_id)
        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
        sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
        possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)

        self.assertTrue(len(possibilities) == len(rooms))

    def testProcessDataDayNotEmpty(self):
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, "2021-10-10", "12b", medic_id)
        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
        sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
        possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)

        self.assertTrue(len(possibilities) >= len(rooms))




# TODO: have to test:
# - preparing possibilities
# - removing colliding possibilities based on working hours
# - sorting
