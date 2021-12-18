from django.urls import path
from .views import (
    all_patients,
    create_patient,
    patient_by_id,
    update_patient,
    delete_patient,

    medic_by_id,
    all_medics,

    all_operations,
    operation_by_id,

    all_rooms,
    room_by_id,

    all_operation_types,
    operation_type_by_id,

    all_NAMs,
    NAM_by_id,

    all_NARs,
    NAR_by_id,

)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView, BlacklistTokenView

from rest_framework.schemas import get_schema_view

from django.views.generic import TemplateView


urlpatterns = [
    path('patients/', all_patients, name='patients'),
    path('create_patient/', create_patient, name='create_patients'),
    path('patient/<id>/', patient_by_id, name='patient'),
    path('update_patient/<id>/', update_patient, name='update_patient'),
    path('delete_patient/<id>/', delete_patient, name='delete_patient'),

    path('medic/<id>/', medic_by_id, name='medic'),
    path('medics/', all_medics, name='medics'),

    path('operations/', all_operations, name='medics'),
    path('operation/<id>/', operation_by_id, name='medic'),

    path('rooms/', all_rooms, name='rooms'),
    path('rooms/<id>/', room_by_id, name='room'),

    path('operation_types/', all_operation_types, name='operation_types'),
    path('operation_type/<id>/', operation_type_by_id, name='operation_type'),

    path('not_available_rooms/', all_NARs, name='operation_types'),
    path('not_available_room/<id>/', NAR_by_id, name='operation_type'),

    path('not_available_medics/', all_NAMs, name='operation_types'),
    path('not_available_medic/<id>/', NAM_by_id, name='operation_type'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),


    # api documentation for development purposes
    path('schema/', get_schema_view(
        title="eOddział",
        description="API documentation for eOddział",
        version="1.0.0"
    ),  name='openapi-schema'),

    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ),  name='swagger-ui'),
]