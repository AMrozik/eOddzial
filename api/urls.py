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

from rest_framework.schemas import get_schema_view

from django.views.generic import TemplateView


urlpatterns = [
    path('patients/', PatientsView.as_view(), name='patients'),
    path('create_patient/', CreatePatientsView.as_view(), name='create_patients'),
    path('patient/<id>/', patient_by_id, name='patient'),
    path('update_patient/<id>/', update_patient, name='update_patient'),
    path('delete_patient/<id>/', delete_patient, name='delete_patient'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),


    # api documentation for development purposes
    path('schema/', get_schema_view(
        title="eOddział",
        description="API documentation for eOddział",
        version="1.0.0"
    ), name='openapi-schema'),

    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]