from django.shortcuts import render
from django.http import HttpResponse
from .serializers import PatientSerializer
from .models import PatientModel
from rest_framework import generics


# Create your views here.
class PatientsView(generics.ListAPIView):
    queryset = PatientModel.objects.all()
    serializer_class = PatientSerializer


class CreatePatientsView(generics.CreateAPIView):
    queryset = PatientModel.objects.all()
    serializer_class = PatientSerializer
