import datetime
from django.test import TestCase
from .models import WardData
from .utils.ALG import DailyHintALG
from .models import Operation
from .models import Operation_type
from .models import Medic
from .models import Patient
from .models import Room

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

        # TODO: query ammount of rooms in ward
        self.assertTrue(len(sorted_list) == 2)

    def testSortingByRoomsNotEquals(self):
        algorithm = DailyHintALG(True, "2021-10-10", "12b")
        (daily_operations, operation_type) = algorithm.gatherDataFromDB()

        sorted_list = algorithm.sortListBasedOnRooms(daily_operations)

        # TODO: query ammount of rooms in ward
        self.assertFalse(len(sorted_list) != 2)
