import datetime
from statistics import mean
from api.models import Operation_type, BudgetYear
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
    # data["nie_wyk_int"] = 0
    # for operation in operations:
    #     if not operation.done:
    #         data["nie_wyk_int"] += 1
    # data["nie_wyk_proc"] = Decimal(data["nie_wyk_int"])/Decimal(data["zab"])

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
    data["men_proc"] = Decimal(data["men_int"])/Decimal(len(operations)) * 100
    data["kob_proc"] = Decimal(data["kob_int"])/Decimal(len(operations)) * 100

    # Difficulty
    for operation in operations:
        if operation.type.is_difficult:
            data["tru_int"] += 1
    data["tru_proc"] = Decimal(data["tru_int"])/Decimal(len(operations)) * 100

    # Child
    for operation in operations:
        if operation.patient.age < datetime.date.today().year:
            data["dzi_int"] += 1
    data["dzi_proc"] = Decimal(data["dzi_int"])/Decimal(len(operations)) * 100

    # Age
    ages = []
    for operation in operations:
        ages.append(operation.patient.age)
    ages.sort()

    year = datetime.date.today().year
    data["wiek_min_int"] = year - ages[0]
    data["wiek_max_int"] = year - ages[-1]
    data["wiek_sred"] = year - mean(ages)

    return data


def budged(operations, types, start_date, end_date):
    data = {}

    year_amount = end_date.year - start_date.year + 1
    start_month = start_date.month
    end_month = end_date.month

    # Yearly scope budget
    budget_y = 0
    for i in range(year_amount):
        budget_y += BudgetYear.objects.get(year=start_date.year+i).given_budget
    data["bud_rok"] = budget_y

    # Monthly scope budget - is sum of months percentage times yearly budget
    # WARNING!!! This is not checking does monthly percentages sum to more than 1!

    # Prepare months list
    if year_amount > 1:
        months_list = [(start_month, 12)]
        for i in range(year_amount-2):
            months_list.append((1, 12))
        months_list.append((1, end_month))
    else:
        months_list = [(start_month, end_month)]

    budget_m = 0
    for i in range(year_amount):
        year = BudgetYear.objects.get(year=start_date.year+i)
        for month in range(months_list[i][0], months_list[i][1]+1):
            # TODO: get rid of if else and do maybe dict
            if month == 1:
                budget_m += year.given_budget * year.jan
            elif month == 2:
                budget_m += year.given_budget * year.feb
            elif month == 3:
                budget_m += year.given_budget * year.mar
            elif month == 4:
                budget_m += year.given_budget * year.apr
            elif month == 5:
                budget_m += year.given_budget * year.may
            elif month == 6:
                budget_m += year.given_budget * year.jun
            elif month == 7:
                budget_m += year.given_budget * year.jul
            elif month == 8:
                budget_m += year.given_budget * year.aug
            elif month == 9:
                budget_m += year.given_budget * year.sep
            elif month == 10:
                budget_m += year.given_budget * year.oct
            elif month == 11:
                budget_m += year.given_budget * year.nov
            elif month == 12:
                budget_m += year.given_budget * year.dec
    data["bud_mon"] = budget_m

    # Total cost of all operations
    cost = 0
    for operation in operations:
        cost += operation.type.cost
    data["zab_koszt_int"] = cost

    # Operations done/planned amount and percentages of overall operations
    data["wyk_int"] = 0
    data["wyk_koszt_int"] = 0
    data["zap_int"] = 0
    for operation in operations:
        if operation.done:
            # Done
            data["wyk_int"] += 1
            data["wyk_koszt_int"] += operation.type.cost
        else:
            # Planned
            data["zap_int"] += 1
    data["wyk_proc"] = Decimal(data["wyk_int"])/Decimal(len(operations)) * 100
    data["zap_proc"] = Decimal(data["zap_int"])/Decimal(len(operations)) * 100

    # Types of all operations
    types_int = {}
    types_proc = {}
    for key in types.keys():
        types_int[key] = Decimal(Operation_type.objects.filter(ICD_code=key)[0].cost) * Decimal(types[key])
        types_proc[key] = Decimal(types_int[key])/Decimal(cost) * 100

    data["bud_typy_int"] = types_int
    data["bud_typy_proc"] = types_proc

    return data


def getStats(operations, start_date, end_date):
    """

    Args:
        start_date: starting DATE taken from frontend
        end_date: ending DATE taken from frontend
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
    data.update(budged(operations, types, start_date, end_date))

    return data
