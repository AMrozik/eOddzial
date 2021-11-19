import datetime
from api.models import Operation, Operation_type, WardData, Medic, Room


class PossibleOperation:
    def __init__(self, start_hour, is_child, is_difficult, room, in_proper_interval, ward_beginning_hour, ward_ending_hour, ward_child_hour, ward_difficult_hour):
        """

        Args:
            start_hour: HOUR stores operation starting time
            is_child: BOOLEAN storing is patient child
            is_difficult: BOOLEAN sorting is patient's operation difficult
            room: INT representing room for this operation (it helps generate clear JSON)
            in_proper_interval: BOOLEAN representing is operation in designated interval for this operation (for React logic)
            ward_beginning_hour: HOUR ward work starting hour information
            ward_ending_hour: HOUR ward work ending hour information
            ward_child_hour: HOUR ward information about end of child interval
            ward_difficult_hour: HOUR ward information about beginning of difficult interval
        """
        self.start_hour = dateTimeToInt(start_hour)
        self.is_child = is_child
        self.is_difficult = is_difficult
        self.room = room
        self.in_proper_interval = in_proper_interval
        self.ward_ending_hour = dateTimeToInt(ward_ending_hour)
        self.ward_beginning_hour = dateTimeToInt(ward_beginning_hour)
        self.ward_child_hour = dateTimeToInt(ward_child_hour)
        self.ward_difficult_hour = dateTimeToInt(ward_difficult_hour)

    def score(self):
        normal_points = self.start_hour - self.ward_child_hour if self.start_hour < self.ward_child_hour else self.ward_ending_hour - self.start_hour
        child_points = (self.ward_ending_hour - self.start_hour) * self.is_child
        difficulty_points = (self.start_hour - self.ward_difficult_hour) * self.is_difficult
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
    def __init__(self, is_child, is_difficult, day_date, type_ICD, medic_id):
        # Data from REST
        self.is_child = is_child
        self.is_difficult = is_difficult
        self.day_date = day_date
        self.type_ICD = type_ICD
        self.medic_id = medic_id

        # Data about ward
        ward_data = WardData.objects.all()[0]
        self.operation_prepare_time = ward_data.operation_prepare_time
        self.ward_beginning_hour = ward_data.working_start_hour
        self.ward_ending_hour = ward_data.working_end_hour
        self.ward_child_hour = ward_data.child_interval_hour
        self.ward_difficult_hour = ward_data.difficult_interval_hour

    def gatherDataFromDB(self):
        """

        Returns:
            daily_operations: LIST of OPERATION objects from selected day
            operation_type: OPERATION_TYPE object of selected type
            medic: MEDIC object of selected medic

        """
        daily_operations = Operation.objects.raw("SELECT * FROM api_operation WHERE date = %s", [self.day_date])
        operation_type = Operation_type.objects.get(ICD_code=self.type_ICD)
        medic = Medic.objects.get(id=self.medic_id)
        rooms = Room.objects.all()
        return daily_operations, operation_type, medic, rooms

    def sortListBasedOnRooms(self, daily_operations, rooms):
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
        # TODO: append empty list for room with no operations ;)

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

        # Make sure that room sorted list has one list for each room
        empty_rooms = len(rooms)-len(room_operation_list)
        for i in range(empty_rooms):
            temp_list = []
            room_operation_list.append(temp_list)

        return room_operation_list

    def checkIsInInterval(self, hour):
        """

        Args:
            hour: Starting hour of operation that you want to check

        Returns:
            BOOLEAN with information is hour in it's interval

        """
        is_in_interval = False
        if self.is_child and hour < dateTimeToInt(self.ward_child_hour):
            is_in_interval = True
        elif self.is_difficult and hour > dateTimeToInt(self.ward_difficult_hour):
            is_in_interval = True
        elif self.is_child is False and self.is_difficult is False and dateTimeToInt(self.ward_child_hour) < hour < dateTimeToInt(self.ward_difficult_hour):
            is_in_interval = True

        return is_in_interval

    def processData(self, room_sorted_list, medic, duration, room_list):
        # ONLY IF NEEDED, ELSE DELETE
        # operation_types = Operation_type.objects.all()

        # Special rule for child with difficult case
        # if is_child and is_difficult:
        #     TODO: Prepare only one PossibleOperation for each room which is in child interval and proceed with JSON else process data normaly

        possibilities = []
        for i, room_operations in enumerate(room_sorted_list):

            # Add possibilities on beginning of each interval and each room
            is_in_interval = self.checkIsInInterval(dateTimeToInt(self.ward_beginning_hour))
            possibilities.append(PossibleOperation(self.ward_beginning_hour, self.is_child, self.is_difficult,
                                                   room_list[i].room_number, is_in_interval,
                                                   self.ward_beginning_hour, self.ward_ending_hour,
                                                   self.ward_child_hour, self.ward_difficult_hour))
            is_in_interval = self.checkIsInInterval(dateTimeToInt(self.ward_child_hour))
            possibilities.append(PossibleOperation(self.ward_child_hour, self.is_child, self.is_difficult,
                                                   room_list[i].room_number, is_in_interval,
                                                   self.ward_beginning_hour, self.ward_ending_hour,
                                                   self.ward_child_hour, self.ward_difficult_hour))
            is_in_interval = self.checkIsInInterval(dateTimeToInt(self.ward_difficult_hour))
            possibilities.append(PossibleOperation(self.ward_difficult_hour, self.is_child, self.is_difficult,
                                                   room_list[i].room_number, is_in_interval,
                                                   self.ward_beginning_hour, self.ward_ending_hour,
                                                   self.ward_child_hour, self.ward_difficult_hour))

            # Add possibilities between already exiting operations and after them
            for j, operation in enumerate(room_operations):
                # Check time between next operations
                if j+1 < len(room_sorted_list):
                    free_time = dateTimeToInt(room_operations[j].start) + int(room_operations[j].type.duration.total_seconds()) - dateTimeToInt(room_operations[j+1].start)
                    # Is it possible to place new operation here?
                    if free_time + dateTimeToInt(self.operation_prepare_time) > int(duration.total_seconds()):
                        possible_operation_start_hour = dateTimeToInt(room_operations[j].start) + int(room_operations[j].type.duration.total_seconds()) + dateTimeToInt(self.operation_prepare_time)
                        # Check is operation in proper interval to pass it to constructor
                        is_in_interval = self.checkIsInInterval(possible_operation_start_hour)
                        # YES: add this possibility to list
                        possible_operation_start_hour = intToDateTime(possible_operation_start_hour)
                        possibilities.append(PossibleOperation(possible_operation_start_hour, self.is_child,
                                                               self.is_difficult, room_operations[0].room.room_number,
                                                               is_in_interval, self.ward_beginning_hour,
                                                               self.ward_ending_hour, self.ward_child_hour,
                                                               self.ward_difficult_hour))

            # Add possibility on the end of not empty list
            if room_operations:
                possible_operation_start_hour = dateTimeToInt(room_operations[-1].start) + int(room_operations[-1].type.duration.total_seconds()) + dateTimeToInt(self.operation_prepare_time)
                possible_operation_start_hour = intToDateTime(possible_operation_start_hour)
                possibilities.append(PossibleOperation(possible_operation_start_hour, self.is_child, self.is_difficult,
                                                       room_operations[0].room.room_number, is_in_interval,
                                                       self.ward_beginning_hour, self.ward_ending_hour,
                                                       self.ward_child_hour, self.ward_difficult_hour))

        # Select possibilities if they are not in range of medic working hours
        to_remove = []
        for possibility in possibilities:
            if dateTimeToInt(medic.work_start) > possibility.start_hour > dateTimeToInt(medic.work_end):
                to_remove.append(possibility)

        # Select possibilities if they collide with already appointed operations
        for room_operations in room_sorted_list:
            for operation in room_operations:
                for possibility in possibilities:
                    if dateTimeToInt(operation.start) <= possibility.start_hour <= dateTimeToInt(operation.start) + int(operation.type.duration.total_seconds()):
                        to_remove.append(possibility)

        # Select possibilities if they collide with medic's operations in this day
        medic_operations = Operation.objects.filter(medic=medic)
        for medic_operation in medic_operations:
            for possibility in possibilities:
                if dateTimeToInt(medic_operation.start) < possibility.start_hour < (dateTimeToInt(medic_operation.start) + int(medic_operation.type.duration.total_seconds())):
                    to_remove.append(possibility)

        # Removing operations
        for operation in to_remove:
            if operation in possibilities:
                possibilities.remove(operation)

        # Sort possibilities to get best results on top
        possibilities.sort()

        print(len(possibilities))

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


def dateTimeToInt(date_time):
    """

    Args:
        date_time: DATETIME.TIME object to converse

    Returns:
        INT value from dateTime.time in seconds

    """
    time = 0
    time += int(date_time.hour)*60*60
    time += int(date_time.minute)*60
    time += int(date_time.second)
    return time


def intToDateTime(value):
    """

    Args:
        value: INT value in seconds to converse to dateTime.time

    Returns:
        DATETIME.TIME object from values

    """
    hours = int(value / 3600)
    value -= hours * 3600
    minutes = int(value / 60)
    value -= minutes * 60
    seconds = value
    return datetime.time(hour=hours, minute=minutes, second=seconds)
