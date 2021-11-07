from django.urls import path
from .views import (
    PatientsView,
    CreatePatientsView,
    patient_by_id,
    update_patient,
    delete_patient,
)


urlpatterns = [
    path('patients/', PatientsView.as_view(), name='patients'),
    path('create_patient/', CreatePatientsView.as_view(), name='create_patients'),
    path('patient/<id>/', patient_by_id, name='patient'),
    path('update_patient/<id>/', update_patient, name='update_patient'),
    path('delete_patient/<id>/', delete_patient, name='delete_patient'),
]