from json import dumps, loads, JSONEncoder
from api.models import Operation

def getPercenteges(year):
    # gather all operations
    operations = Operation.object.all()

    # filter for year
    # sort by day
    # convert to percentages
    return 0
