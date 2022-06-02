import datetime
from json import dumps, loads, JSONEncoder
from api.models import Operation, OperationType, WardData, Medic, Room


class PossibleOperation:
    def __init__(self, start_hour, is_child, is_difficult, room, in_proper_interval, ward_beginning_hour,
                 ward_ending_hour, ward_child_hour, ward_difficult_hour, day_date):
        """

        Args:
            start_hour: DATETIME stores operation starting time
            is_child: BOOLEAN storing is patient child
            is_difficult: BOOLEAN sorting is patient's operation difficult
            room: INT representing room for this operation (it helps generate clear JSON)
            in_proper_interval: BOOLEAN representing is operation in designated interval for this operation (for React)
            ward_beginning_hour: INT ward work starting hour information
            ward_ending_hour: INT ward work ending hour information
            ward_child_hour: INT ward information about end of child interval
            ward_difficult_hour: INT ward information about beginning of difficult interval
            day_date: DATETIME with the day of operation
        """
        self.start = datetime.datetime(year=day_date.year, month=day_date.month, day=day_date.day, hour=start_hour.hour,
                                       minute=start_hour.minute, second=start_hour.second)
        self.is_child = is_child
        self.is_difficult = is_difficult
        self.room = room
        self.in_proper_interval = in_proper_interval
        # Only for easier score calculation
        self.start_hour = datetime_to_int(start_hour)
        self.ward_ending_hour = datetime_to_int(ward_ending_hour)
        self.ward_beginning_hour = datetime_to_int(ward_beginning_hour)
        self.ward_child_hour = datetime_to_int(ward_child_hour)
        self.ward_difficult_hour = datetime_to_int(ward_difficult_hour)

    def score(self):
        normal_points = self.start_hour - self.ward_child_hour if self.start_hour < self.ward_child_hour \
            else self.ward_ending_hour - self.start_hour
        child_points = (self.ward_ending_hour - self.start_hour) * self.is_child
        difficulty_points = (self.start_hour - self.ward_difficult_hour) * self.is_difficult
        return child_points * 10 + normal_points + difficulty_points * 10

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

    def to_json(self):
        """

        Returns:
            DICT with only needed data about form this object

        """
        result = self.__dict__
        del result['start_hour']
        del result['ward_ending_hour']
        del result['ward_beginning_hour']
        del result['ward_child_hour']
        del result['ward_difficult_hour']

        result['start'] = result['start'].isoformat("T")

        return result


class DailyHintALG:
    def __init__(self, is_child, is_difficult, day_date, type_icd, medic_id):

        # Data from REST
        self.is_child = is_child
        self.is_difficult = is_difficult
        self.day_date = day_date
        self.type_ICD = type_icd
        self.medic_id = medic_id

        # Data about ward
        ward_data = WardData.objects.all()[0]
        self.operation_prepare_time = ward_data.operation_prepare_time
        self.ward_beginning_hour = ward_data.working_start_hour
        self.ward_ending_hour = ward_data.working_end_hour
        self.ward_child_hour = ward_data.child_interval_hour
        self.ward_difficult_hour = ward_data.difficult_interval_hour

    def gather_data_from_db(self):
        """

        Returns:
            daily_operations: LIST of OPERATION objects from selected day
            operation_type: OPERATION_TYPE object of selected type
            medic: MEDIC object of selected medic

        """
        # TODO: Make this safe from front end point of view !!!!
        daily_operations = Operation.objects.raw("SELECT * FROM api_operation WHERE date = %s", [self.day_date])
        operation_type = OperationType.objects.get(ICD_code=self.type_ICD)
        medic = Medic.objects.get(id=self.medic_id)
        rooms = Room.objects.all()
        return daily_operations, operation_type, medic, rooms

    def sort_list_based_on_rooms(self, daily_operations, rooms):
        """

        Args:
            daily_operations: QUERYSET with all operations in defined day
            rooms:

        Returns:
            LIST[LIST[INT]] with operations sorted based on room they are expected to be

        """
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

        # Make sure that room sorted list has at least one list for each room
        empty_rooms = len(rooms) - len(room_operation_list)
        for i in range(empty_rooms):
            temp_list = []
            room_operation_list.append(temp_list)

        return room_operation_list

    def check_is_in_interval(self, hour):
        """

        Args:
            hour: DATETIME.TIME object with starting hour of operation that you want to check

        Returns:
            BOOLEAN with information is hour in it's interval

        """
        is_in_interval = False

        if self.is_child and not self.is_difficult and hour < datetime_to_int(self.ward_child_hour) \
                or not self.is_child and self.is_difficult and hour >= datetime_to_int(self.ward_difficult_hour) \
                or self.is_child and self.is_difficult \
                or not self.is_child and not self.is_difficult and \
                datetime_to_int(self.ward_child_hour) <= hour < datetime_to_int(self.ward_difficult_hour):
            is_in_interval = True

        return is_in_interval

    def prepare_possibilities(self, room_sorted_list, room_list, duration):
        """

        Args:
            room_sorted_list: LIST[LIST[INT]] with operations sorted based on rooms
            room_list: LIST[INT] with stored integer values of rooms in ward
            duration: DATETIME.TIME with duration of this operation

        Returns:

        """
        possibilities = []

        # Special rule for child with difficult case
        if self.is_child and self.is_difficult:
            for i, room in enumerate(room_sorted_list):
                possibilities.append(PossibleOperation(self.ward_beginning_hour, self.is_child, self.is_difficult,
                                                       room_list[i].room_number, True,
                                                       self.ward_beginning_hour, self.ward_ending_hour,
                                                       self.ward_child_hour, self.ward_difficult_hour,
                                                       self.day_date))
        else:
            for i, room_operations in enumerate(room_sorted_list):

                # Add possibilities on beginning of each interval and each room
                is_in_interval = self.check_is_in_interval(datetime_to_int(self.ward_beginning_hour))
                possibilities.append(PossibleOperation(self.ward_beginning_hour, self.is_child, self.is_difficult,
                                                       room_list[i].room_number, is_in_interval,
                                                       self.ward_beginning_hour, self.ward_ending_hour,
                                                       self.ward_child_hour, self.ward_difficult_hour,
                                                       self.day_date))
                is_in_interval = self.check_is_in_interval(datetime_to_int(self.ward_child_hour))
                possibilities.append(PossibleOperation(self.ward_child_hour, self.is_child, self.is_difficult,
                                                       room_list[i].room_number, is_in_interval,
                                                       self.ward_beginning_hour, self.ward_ending_hour,
                                                       self.ward_child_hour, self.ward_difficult_hour,
                                                       self.day_date))
                is_in_interval = self.check_is_in_interval(datetime_to_int(self.ward_difficult_hour))
                possibilities.append(PossibleOperation(self.ward_difficult_hour, self.is_child, self.is_difficult,
                                                       room_list[i].room_number, is_in_interval,
                                                       self.ward_beginning_hour, self.ward_ending_hour,
                                                       self.ward_child_hour, self.ward_difficult_hour,
                                                       self.day_date))

                # Add possibilities between already existing operations and after them
                for j, operation in enumerate(room_operations):
                    # Check time between next operations
                    if j + 1 < len(room_operations):
                        free_time = datetime_to_int(room_operations[j].start) + int(
                            room_operations[j].type.duration.total_seconds()) - datetime_to_int(
                            room_operations[j + 1].start)
                        # Is it possible to place new operation here?
                        if free_time + datetime_to_int(self.operation_prepare_time) > int(duration.total_seconds()):
                            possible_operation_start_hour = datetime_to_int(room_operations[j].start) + int(
                                room_operations[j].type.duration.total_seconds()) + datetime_to_int(
                                self.operation_prepare_time)
                            # Check is operation in proper interval to pass it to constructor
                            is_in_interval = self.check_is_in_interval(possible_operation_start_hour)
                            # YES: add this possibility to list
                            possible_operation_start_hour = int_to_datetime(possible_operation_start_hour)
                            possibilities.append(PossibleOperation(possible_operation_start_hour, self.is_child,
                                                                   self.is_difficult,
                                                                   room_operations[0].room.room_number,
                                                                   is_in_interval, self.ward_beginning_hour,
                                                                   self.ward_ending_hour, self.ward_child_hour,
                                                                   self.ward_difficult_hour, self.day_date))

                # Add possibility on the end of not empty list
                if room_operations:
                    possible_operation_start_hour = datetime_to_int(room_operations[-1].start) + int(
                        room_operations[-1].type.duration.total_seconds()) + datetime_to_int(
                        self.operation_prepare_time)
                    possible_operation_start_hour = int_to_datetime(possible_operation_start_hour)
                    possibilities.append(
                        PossibleOperation(possible_operation_start_hour, self.is_child, self.is_difficult,
                                          room_operations[0].room.room_number, is_in_interval,
                                          self.ward_beginning_hour, self.ward_ending_hour,
                                          self.ward_child_hour, self.ward_difficult_hour,
                                          self.day_date))

        return possibilities

    def remove_invalid_possibilities(self, possibilities, medic, room_sorted_list):
        """

        Args:
            possibilities: LIST[POSSIBLEOPERATION] to remove invalid possibilities from
            medic: MEDIC object storing data for this operation medic
            room_sorted_list: LIST[LIST[INT]] with operations sorted based on rooms

        Returns:
            LIST[POSSIBLEOPERATION] without invalid possibilities

        """
        to_remove = []

        # Select possibilities if they are not in range of ward working hours
        for possibility in possibilities:
            if datetime_to_int(self.ward_beginning_hour) > possibility.start_hour > datetime_to_int(
                    self.ward_ending_hour):
                to_remove.append(possibility)

        # Select possibilities if they collide with already appointed operations
        for room_operations in room_sorted_list:
            for operation in room_operations:
                for possibility in possibilities:
                    if operation.room.room_number == possibility.room:
                        if datetime_to_int(operation.start) <= possibility.start_hour <= datetime_to_int(
                                operation.start) + int(operation.type.duration.total_seconds()):
                            to_remove.append(possibility)

        # Select possibilities if they collide with medic's operations in this day
        medic_operations = Operation.objects.filter(medic=medic)
        for medic_operation in medic_operations:
            for possibility in possibilities:
                if datetime_to_int(medic_operation.start) < possibility.start_hour < (
                        datetime_to_int(medic_operation.start) + int(medic_operation.type.duration.total_seconds())):
                    to_remove.append(possibility)

        # Removing operations
        for operation in to_remove:
            if operation in possibilities:
                possibilities.remove(operation)

        return possibilities

    def process_data(self, room_sorted_list, medic, duration, room_list):
        """

        Args:
            room_sorted_list: LIST[LIST[INT]] with operations sorted based on rooms'
            medic: MEDIC object storing data for this operation medic
            duration: DATETIME.TIME with duration of this operation
            room_list: LIST[INT] with stored integer values of rooms in ward

        Returns:
            LIST[POSSIBLE_OPERATION] sorted based on their score

        """
        # Preparing possibilities
        possibilities = self.prepare_possibilities(room_sorted_list, room_list, duration)
        # Removing invalid possibilities
        possibilities = self.remove_invalid_possibilities(possibilities, medic, room_sorted_list)
        # Sort possibilities to get best results on top
        possibilities.sort(reverse=True)

        return possibilities

    def to_json(self):
        """

        Returns:
            JSON out of sorted list with possible operations

        """
        # Gather data from DB
        (daily_operations, operation_type, medic, rooms) = self.gather_data_from_db()

        # Prepare data for algorithm
        room_sorted_list = self.sort_list_based_on_rooms(daily_operations, rooms)

        # Process data with algorithm
        sorted_possibilities = self.process_data(room_sorted_list, medic, operation_type.duration, rooms)

        return loads(dumps(sorted_possibilities, cls=ListOfPossibleOptionsEncoder))


# UTILITY SECTION (not worth it to make in different file)
def datetime_to_int(date_time):
    """

    Args:
        date_time: DATETIME.TIME object to converse

    Returns:
        INT value from dateTime.time in seconds

    """
    time = 0
    time += int(date_time.hour) * 60 * 60
    time += int(date_time.minute) * 60
    time += int(date_time.second)
    return time


def int_to_datetime(value):
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


class ListOfPossibleOptionsEncoder(JSONEncoder):
    def default(self, o):
        return o.to_json()
