from django.urls import path
from .views import (
    PatientsView,
    CreatePatientsView,
    patient_by_id,
    update_patient,
    delete_patient,
)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView, BlacklistTokenView


urlpatterns = [
    path('patients/', PatientsView.as_view(), name='patients'),
    path('create_patient/', CreatePatientsView.as_view(), name='create_patients'),
    path('patient/<id>/', patient_by_id, name='patient'),
    path('update_patient/<id>/', update_patient, name='update_patient'),
    path('delete_patient/<id>/', delete_patient, name='delete_patient'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistTokenView.as_view(), name="logout")
]