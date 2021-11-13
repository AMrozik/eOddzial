from api.models import Operation, Operation_type, WardData, Medic


class PossibleOperation:
    def __init__(self, start_hour, is_child, difficulty, room, ward_beginning_hour, ward_ending_hour, ward_child_hour, ward_difficult_hour):
        """

        Args:
            start_hour: operation start hour in seconds format
            is_child:
            difficulty:
            room: ward room for operation
            ward_ending_hour: end hour of work in this ward
            ward_beginning_hour: beginning hour of work for this ward
            ward_child_hour: last hour reserved for child operations
            ward_difficult_hour: first hour in interval for difficult operations
        """
        self.start_hour = start_hour
        self.is_child = is_child
        self.difficulty = difficulty
        self.room = room
        self.ward_ending_hour = ward_ending_hour
        self.ward_beginning_hour = ward_beginning_hour
        self.ward_child_hour = ward_child_hour
        self.ward_difficult_hour = ward_difficult_hour

    def score(self):
        # TODO: testing
        normal_points = self.start_hour - self.ward_child_hour if self.start_hour < self.ward_child_hour else self.ward_ending_hour - self.start_hour
        child_points = (self.ward_ending_hour - self.start_hour) * self.is_child
        difficulty_points = (self.start_hour - self.ward_difficult_hour) * self.difficulty
        return child_points + normal_points + difficulty_points

    def __lt__(self, other):
        return self.score() < other.score()

    def __le__(self, other):
        return self.score() <= other.score()

    def __eq__(self, other):
        return self.score() == other.score()

    def __ne__(self, other):
        return self.score() != other.score()

    def __gt__(self, other):
        return self.score() > other.score()

    def __ge__(self, other):
        return self.score() >= other.score()


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

            iterator = 0
            while iterator < len(daily_operations_list):
                if daily_operations_list[iterator].room.room_number == room:
                    temp_list.append(daily_operations_list[iterator])
                    daily_operations_list.remove(daily_operations_list[iterator])
                else:
                    iterator += 1

            room_operation_list.append(temp_list)

        return room_operation_list

    def processData(self, room_sorted_list, lekarz_ID, czy_dziecko, czy_trudne, duration):
        # ONLY IF NEEDED, ELSE DELETE
        # operation_types = Operation_type.objects.all()

        possibilities = []
        for room_operations in enumerate(room_sorted_list):
            for i, operation in enumerate(room_operations):
                # Check time between next operations
                if i+1 < len(room_sorted_list):
                    free_time = room_operations[i].start + room_operations[i].type.duration - room_operations[i+1].start
                    # Is it possible to place new operation here?
                    if free_time + self.operation_prepare_time > duration:
                        # YES: add this possibility to list
                        possibilities.append(PossibleOperation())

        # Wyrzuc operacje jezeli nie sa w godzinach pracy lekarza

        # Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie
        # TODO: poprawic sprawdzanie przy operacjach dnia
        for operacja in operacje_dnia:
            for i,mozliwosc in enumerate(mozliwosci):
                if mozliwosc[godzina] == operacja[godzina]:
                    if mozliwosc[lekarz] == operacja[lekarz]:
                        del(mozliwosci[i])

        # Sort possibilities to get best results on top
        possibilities.sort()

        return possibilities

    def toJson(self):
        # Gather data from DB
        (daily_operations, operation_type) = self.gatherDataFromDB()

        # Prepare data for algorithm
        room_sorted_list = self.sortListBasedOnRooms(daily_operations)

        # Process data with algorithm
        # sorted_possibilities = processData()

        # Prepare JSON out of possibilities
        return 0
