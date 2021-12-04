import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .serializers import PatientSerializer
from .models import Patient
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.ALG import DailyHintALG


# Create your views here.
class PatientsView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class CreatePatientsView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


@api_view(["POST"])
def dailyAlg(request):
    """

    Args:
        request: POST request with isChild, isDifficult, year, month, day, type and medic information

    Returns:
        Valid, sorted JSON with data about possible operations

    """
    if request.method == "POST":
        is_child = request.POST.get("is_child")             # 1 or 0
        is_difficult = request.POST.get("is_difficult")     # 1 or 0
        date_year = request.POST.get("date_year")           # int
        date_month = request.POST.get("date_month")         # int
        date_day = request.POST.get("date_day")             # int
        type_ICD = request.POST.get("type_ICD")             # int
        medic_id = request.POST.get("medic_id")             # int

        if is_child is None or is_difficult is None or date_year is None or date_month is None or date_day is None or type_ICD is None or medic_id is None:
            return Response(status= status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            day_date = datetime.date(year=int(date_year), month=int(date_month), day=int(date_day))
            algorithm = DailyHintALG(int(is_child), int(is_difficult), day_date, type_ICD, medic_id)

            json = algorithm.toJSON()

            return Response(status=status.HTTP_200_OK, data=json)

    return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)

