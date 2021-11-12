from django.shortcuts import render
from django.http import HttpResponse
from .serializers import PatientSerializer
from .models import Patient
from rest_framework import generics, status
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
    if request.method == "POST":
        is_child = request.POST.get("is_child", None)
        day_date = request.POST.get("day_date", "0-0-0")
        type_ICD = request.POST.get("type_ICD", -1)
        medic_id = request.POST.get("medic_id", -1)

        algorithm = DailyHintALG(is_child, day_date, type_ICD, medic_id)
        json = algorithm.toJson()
        return Response(status= status.HTTP_200_OK, data=json)

    return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)

