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
    edit_operations,
    operation_by_id,
    edit_operation_by_id,

    all_rooms,
    room_by_id,

    all_operation_types,
    operation_type_by_id,

    all_nams,
    nam_by_id,

    all_nars,
    nar_by_id,
    active_rooms,

    view_logs,
    view_logs_by_id,

    daily_alg,
    medic_presence,
    yearly_alg,
    statistics,
    update_ward_data,
    create_ward_data,
    budget_years,
    budget_year,

)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView, BlacklistTokenView

from rest_framework.schemas import get_schema_view

from django.views.generic import TemplateView


urlpatterns = [
    path('patients/', all_patients, name='patients'),
    path('create_patient/', create_patient, name='create_patients'),
    path('patient/<_id>/', patient_by_id, name='patient'),
    path('update_patient/<_id>/', update_patient, name='update_patient'),
    path('delete_patient/<_id>/', delete_patient, name='delete_patient'),

    path('medic/<_id>/', medic_by_id, name='medic'),
    path('medics/', all_medics, name='medics'),

    path('operations/', all_operations, name='operations'),
    path('operations/edit/', edit_operations, name='edit_operations'),
    path('operation/<_id>/', operation_by_id, name='operations_by_id'),
    path('operation/<_id>/edit/', edit_operation_by_id, name='operation_edit_by_id'),

    path('rooms/', all_rooms, name='rooms'),
    path('rooms/<_id>/', room_by_id, name='room'),
    path('rooms/active/', active_rooms, name='active_rooms'),

    path('operation_types/', all_operation_types, name='operation_types'),
    path('operation_type/<_id>/', operation_type_by_id, name='operation_type'),

    path('not_available_rooms/', all_nars, name='not_available_rooms'),
    path('not_available_room/<_id>/', nar_by_id, name='not_available_room'),

    path('not_available_medics/', all_nams, name='not_available_medics'),
    path('not_available_medic/<_id>/', nam_by_id, name='not_available_medic'),

    path('ward_data/', update_ward_data, name='ward_data'),
    path('create_ward_data/', create_ward_data, name='create_ward_data'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),

    # Logs
    path('logs/', view_logs, name='logs'),
    path('logs/<_id>', view_logs_by_id, name='log'),

    # Hint Alg
    path('dailyAlg/', daily_alg, name='dailyAlg'),
    path('yearlyAlg/', yearly_alg, name='yearlyAlg'),

    # MedicPresence
    path('medicPresence/', medic_presence, name='medicPresence'),

    # statistics
    path('statistics/', statistics, name='statistics'),

    # budget years
    path('budget_years/', budget_years, name='budgetYears'),
    path('budget_year/<year>/', budget_year, name='budgetYear'),


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