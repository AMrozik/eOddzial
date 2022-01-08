import datetime
from statistics import mean
from api.models import Operation_type, BudgetMonth, BudgetYear
from decimal import *


def procedures(operations, types):

    # Procedures
    data = {"zab": len(operations)}

    # Types
    types_proc = {}
    for key in types.keys():
        types_proc[key] = Decimal(types[key]) / Decimal(data["zab"])
    data["zab_typy_int"] = types
    data["zab_typy_proc"] = types_proc

    # Not done operations
    data["ndone_int"] = 0
    for operation in operations:
        if not operation.done:
            data["ndone_int"] += 1
    data["ndone_proc"] = Decimal(data["ndone_int"])/Decimal(data["zab"])

    return data


def patients(operations):
    data = {"men_int": 0,
            "kob_int": 0,
            "dzi_int": 0,
            "tru_int": 0,
            "wiek_min_int": 0,
            "wiek_max_int": 0,
            "wiek_sred": 0,
            }
    # Filling dictionary with values
    # Gender
    for operation in operations:
        if operation.patient.gender == "male":
            data["men_int"] += 1
        else:
            data["kob_int"] += 1
    data["men_proc"] = Decimal(data["men_int"])/Decimal(len(operations))
    data["kob_proc"] = Decimal(data["kob_int"])/Decimal(len(operations))

    # Difficulty
    for operation in operations:
        if operation.type.is_difficult == "True":
            data["tru_int"] += 1
    data["tru_proc"] = Decimal(data["tru_int"])/Decimal(len(operations))

    # Child
    for operation in operations:
        if operation.patient.age < 18:
            data["dzi_int"] += 1
    data["dzi_proc"] = Decimal(data["dzi_int"])/Decimal(len(operations))

    # Age
    ages = []
    for operation in operations:
        ages.append(operation.patient.age)
    ages.sort()
    data["wiek_min_int"] = ages[0]
    data["wiek_max_int"] = ages[-1]
    data["wiek_sred"] = mean(ages)

    return data


def budged(operations, types):
    data = {}

    temp_list = list(operations)
    # start_year = temp_list[0].date.year()
    # end_year = temp_list[-1].date.year()

    # Budget
    budget = 0
    for i in range(temp_list[0].date.year - temp_list[-1].date.year + 1):
        for month in range(1, 13):
            print(f'year:{i}, month:{month}')
            if month == 1:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).jan
            elif month == 2:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).feb
            elif month == 3:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).mar
            elif month == 4:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).apr
            elif month == 5:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).may
            elif month == 6:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).jun
            elif month == 7:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).jul
            elif month == 8:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).aug
            elif month == 9:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).sep
            elif month == 10:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).oct
            elif month == 11:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).nov
            elif month == 12:
                budget += BudgetYear.objects.get(year=temp_list[0].date.year+i).value * BudgetMonth.objects.get(year=temp_list[0].date.year).dec
    data["bud"] = budget

    # Total cost
    cost = 0
    for operation in operations:
        cost += operation.type.cost
    data["cos"] = cost

    # Operations
    data["wyk_int"] = 0
    data["zap_int"] = 0
    for operation in operations:
        if operation.date < datetime.date.today():
            # Done
            data["wyk_int"] += 1
        else:
            # Planned
            data["zap_int"] += 1
    data["wyk_proc"] = Decimal(data["wyk_int"])/Decimal(len(operations))
    data["zap_proc"] = Decimal(data["zap_int"])/Decimal(len(operations))

    # Types
    types_int = {}
    types_proc = {}
    for key in types.keys():
        types_int[key] = Decimal(Operation_type.objects.filter(ICD_code=key)[0].cost) * Decimal(types[key])
        types_proc[key] = Decimal(types_int[key])/Decimal(cost)

    data["bud_typy_int"] = types_int
    data["bud_typy_proc"] = types_proc

    return data


def getStats(operations):
    """

    Args:
        operations: QUERYSET with already filtered operations

    Returns:
        DICTIONARY with statistics of ward

    """
    getcontext().prec = 2

    data = {}

    # storing types of operations
    types = {}
    for operation in operations:
        types[operation.type.ICD_code] = 0
    for operation in operations:
        types[operation.type.ICD_code] += 1

    data.update(procedures(operations, types))
    data.update(patients(operations))
    data.update(budged(operations, types))

    return data
