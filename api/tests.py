import datetime

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
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)
        self.assertTrue(algorithm.is_child)
        self.assertEqual(algorithm.day_date, day)
        self.assertEqual(algorithm.type_ICD, "12b")

    # -----------------------------------------------------------------------------------------------------------------
    # GATHERING DATA FROM DB TESTS

    def testGatheringDataFromDB(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)

        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date=day))
        self.assertTrue(len(daily_operations) == operations_amount)

        self.assertEqual(operation_type.name, "type2")

        self.assertTrue(medic.name == "Krzysztof")

        rooms_amount = len(Room.objects.all())
        self.assertTrue(len(rooms) == rooms_amount)

    def testGatheringDataFromDBDifferentDay(self):
        day = datetime.date(year=2021, month=10, day=11)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)

        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()

        operations_amount = len(Operation.objects.filter(date=day))
        self.assertTrue(len(daily_operations) == operations_amount)

        self.assertEqual(operation_type.name, "type2")

        self.assertTrue(medic.name == "Krzysztof")

        rooms_amount = len(Room.objects.all())
        self.assertTrue(len(rooms) == rooms_amount)

    # -----------------------------------------------------------------------------------------------------------------
    # SORTING BY ROOMS TESTS

    def testSortingByRoomsEquals(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)
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

    # Uncomment if you now how to properly mock PossibleOperation.score() method
    # @patch('PossibleOperation.score')
    # def testPossibleOperationCMP(self, mock_score):
    #     ward_data = WardData.objects.all()[0]
    #     test = PossibleOperation(12*(60*60), False, False, 2, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     test2 = PossibleOperation(11*(60*60), False, False, 2, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     test3 = PossibleOperation(11*(60*60), False, False, 2, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
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

    # VS SELF
    # Child
    def testPossibleOperationScoreChildInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=7, minute=0, second=0)
        time_start2 = datetime.time(hour=9, minute=0, second=0)

        child1 = PossibleOperation(time_start1, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        child2 = PossibleOperation(time_start2, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(child1 > child2)

    def testPossibleOperationScoreChildInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=11, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        child1 = PossibleOperation(time_start1, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        child2 = PossibleOperation(time_start2, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(child1 > child2)

    def testPossibleOperationScoreChildInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=15, minute=0, second=0)
        time_start2 = datetime.time(hour=16, minute=0, second=0)

        child1 = PossibleOperation(time_start1, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        child2 = PossibleOperation(time_start2, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(child1 > child2)

    def testPossibleOperationScoreChildInChildIntervalAndExtremeValue(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=9, minute=0, second=0)
        time_start2 = datetime.time(hour=10, minute=0, second=0)

        child1 = PossibleOperation(time_start1, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        child2 = PossibleOperation(time_start2, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(child1 > child2)

    # Normal
    def testPossibleOperationScoreNormalInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=8, minute=0, second=0)
        time_start2 = datetime.time(hour=9, minute=0, second=0)

        normal1 = PossibleOperation(time_start1, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        normal2 = PossibleOperation(time_start2, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(normal1 < normal2)

    def testPossibleOperationScoreNormalInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=11, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        normal1 = PossibleOperation(time_start1, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        normal2 = PossibleOperation(time_start2, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(normal1 > normal2)

    def testPossibleOperationScoreNormalInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=15, minute=0, second=0)
        time_start2 = datetime.time(hour=16, minute=0, second=0)

        normal1 = PossibleOperation(time_start1, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        normal2 = PossibleOperation(time_start2, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(normal1 > normal2)

    # Difficult
    def testPossibleOperationScoreDifficultInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=8, minute=0, second=0)
        time_start2 = datetime.time(hour=9, minute=0, second=0)

        difficult1 = PossibleOperation(time_start1, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        difficult2 = PossibleOperation(time_start2, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(difficult1 < difficult2)

    def testPossibleOperationScoreDifficultInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=11, minute=0, second=0)
        time_start2 = datetime.time(hour=12, minute=0, second=0)

        difficult1 = PossibleOperation(time_start1, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        difficult2 = PossibleOperation(time_start2, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(difficult1 < difficult2)

    def testPossibleOperationScoreDifficultInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        ward_data = WardData.objects.all()[0]

        time_start1 = datetime.time(hour=15, minute=0, second=0)
        time_start2 = datetime.time(hour=16, minute=0, second=0)

        difficult1 = PossibleOperation(time_start1, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
        difficult2 = PossibleOperation(time_start2, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)

        self.assertTrue(difficult1 < difficult2)

    # VS OTHERS (testing flexibility of algorithm)
    # Child vs Normal
    # def testPossibleOperationScoreChildVsNormalInChildInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=9, minute=0, second=0)
    #
    #     adult = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > adult)
    #
    # def testPossibleOperationScoreChildVsNormalInNormalInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=12, minute=0, second=0)
    #
    #     adult = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > adult)
    #
    # def testPossibleOperationScoreChildVsNormalInDifficultInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=16, minute=0, second=0)
    #
    #     adult = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > adult)
    #
    # def testPossibleOperationScoreDifficultOutDifficultInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=9, minute=0, second=0)
    #
    #     easy = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     difficult = PossibleOperation(time_start, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(difficult < easy)
    #
    # def testPossibleOperationScoreDifficultInDifficultInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=16, minute=0, second=0)
    #
    #     easy = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     difficult = PossibleOperation(time_start, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(difficult > easy)
    #
    # def testPossibleOperationScoreChildVsNormalInChildInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=9, minute=0, second=0)
    #     time_start2 = datetime.time(hour=12, minute=0, second=0)
    #
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     adult = PossibleOperation(time_start2, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > adult)
    #
    # def testPossibleOperationScoreChildVsNormalOutChildInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=12, minute=0, second=0)
    #
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     adult = PossibleOperation(time_start, False, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > adult)
    #
    # def testPossibleOperationScoreChildVsDifficultInChildInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=9, minute=0, second=0)
    #
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     difficult = PossibleOperation(time_start, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child > difficult)
    #
    # def testPossibleOperationScoreChildVsDifficultInDifficultInterval(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     ward_data = WardData.objects.all()[0]
    #
    #     time_start = datetime.time(hour=16, minute=0, second=0)
    #
    #     child = PossibleOperation(time_start, True, False, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #     difficult = PossibleOperation(time_start, False, True, 0, False, ward_data.working_start_hour, ward_data.working_end_hour, ward_data.child_interval_hour, ward_data.difficult_interval_hour, day)
    #
    #     self.assertTrue(child < difficult)

    # -----------------------------------------------------------------------------------------------------------------
    # IS IN PROPER INTERVAL TESTS
    # DifficultChild
    def testIsInProperIntervalChildDifficultInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)

        time = datetime.time(hour=9, minute=0, second=0)
        self.assertTrue(algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalChildDifficultInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)

        time = datetime.time(hour=12, minute=0, second=0)
        self.assertTrue(algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalChildDifficultInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)

        time = datetime.time(hour=16, minute=0, second=0)
        self.assertTrue(algorithm.checkIsInInterval(dateTimeToInt(time)))

    # Child
    def testIsInProperIntervalChildInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, False, day, "12b", medic_id)

        time = datetime.time(hour=9, minute=0, second=0)
        self.assertTrue(algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalChildInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, False, day, "12b", medic_id)

        time = datetime.time(hour=12, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalChildInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, False, day, "12b", medic_id)

        time = datetime.time(hour=16, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    # Difficult
    def testIsInProperIntervalDifficultInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, True, day, "12b", medic_id)

        time = datetime.time(hour=9, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalDifficultInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, True, day, "12b", medic_id)

        time = datetime.time(hour=12, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalDifficultInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, True, day, "12b", medic_id)

        time = datetime.time(hour=16, minute=0, second=0)
        self.assertTrue( algorithm.checkIsInInterval(dateTimeToInt(time)))

    # Normal
    def testIsInProperIntervalNormalInChildInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, False, day, "12b", medic_id)

        time = datetime.time(hour=9, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalNormalInNormalInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, False, day, "12b", medic_id)

        time = datetime.time(hour=12, minute=0, second=0)
        self.assertTrue(algorithm.checkIsInInterval(dateTimeToInt(time)))

    def testIsInProperIntervalNormalInDifficultInterval(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(False, False, day, "12b", medic_id)

        time = datetime.time(hour=16, minute=0, second=0)
        self.assertTrue(not algorithm.checkIsInInterval(dateTimeToInt(time)))

    # -----------------------------------------------------------------------------------------------------------------
    # PROCESS DATA TESTS

    def testProcessDataDayEmpty(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)
        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
        sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
        possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)

        # Assert if possibilities have at least one possibility for each room
        self.assertTrue(len(possibilities) >= len(rooms))

    def testProcessDataDayNotEmpty(self):
        day = datetime.date(year=2021, month=10, day=10)
        medic_id = Medic.objects.get(name="Krzysztof").id
        algorithm = DailyHintALG(True, True, day, "12b", medic_id)
        (daily_operations, operation_type, medic, rooms) = algorithm.gatherDataFromDB()
        sorted_list = algorithm.sortListBasedOnRooms(daily_operations, rooms)
        possibilities = algorithm.processData(sorted_list, medic, operation_type.duration, rooms)

        self.assertTrue(len(possibilities) >= len(rooms))

    # Test only for development
    # def testTest(self):
    #     day = datetime.date(year=2021, month=10, day=10)
    #     medic_id = Medic.objects.get(name="Krzysztof").id
    #     algorithm = DailyHintALG(False, False, day, "12b", medic_id)
    #
    #     print(algorithm.toJSON())
    #
    #     self.assertTrue(True)
