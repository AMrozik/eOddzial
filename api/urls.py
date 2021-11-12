from django.urls import path
from .views import PatientsView, CreatePatientsView, dailyAlg

urlpatterns = [
    path('patients', PatientsView.as_view(), name='patients'),
    path('create_patient', CreatePatientsView.as_view(), name='create_patients'),
    path('dailyAlg', dailyAlg, name='dailyAlg'),
]