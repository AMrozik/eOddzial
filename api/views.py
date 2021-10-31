from django.shortcuts import render
from django.http import HttpResponse
from .serializers import PatientSerializer
from .models import Patient
from rest_framework import generics


# Create your views here.
class PatientsView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class CreatePatientsView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
