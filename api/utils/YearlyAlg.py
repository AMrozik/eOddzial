import datetime
from json import dumps, loads, JSONEncoder
from api.models import Operation, WardData
from .ALG import datetime_to_int, int_to_datetime


def getPercenteges(year):
    # gather all operations and amount of working hours
    operations = Operation.objects.filter(date__year=year).order_by('date')
    hour_end = WardData.objects.all()[0].working_end_hour
    hour_start = WardData.objects.all()[0].working_start_hour
    hour_amount = datetime_to_int(hour_end) - datetime_to_int(hour_start)
    # hour_amount = datetime.datetime(second=hour_amount)

    # sum hours of operations
    temp_date = operations[0].date
    sorted_list = []
    sum_hours = 0
    for operation in operations:
        if operation.date != temp_date:
            sorted_list.append((temp_date, sum_hours))
            temp_date = operation.date
            sum_hours = 0 + operation.type.duration.total_seconds()
        else:
            sum_hours += operation.type.duration.total_seconds()
    sorted_list.append((temp_date, sum_hours))

    # divide sum_hours/hours
    result_dict = {}
    for date, hour_count in sorted_list:
        percentage = hour_count/hour_amount
        result_dict[str(date)] = percentage

    return result_dict
