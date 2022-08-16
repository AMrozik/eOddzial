from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from functools import wraps
from rest_framework_simplejwt.backends import TokenBackend
from users.models import Account
from django.core.exceptions import ValidationError
from typing import List

import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.ALG import DailyHintALG
from .utils.DoctorPresence import checkPresence
from .utils.YearlyAlg import getPercenteges
from .utils.Stats import get_stats

from api.serializers import (
    PatientSerializer,
    MedicSerializer,
    OperationSerializer,
    OperationTypeSerializer,
    NonAvailabilityMedicSerializer,
    RoomSerializer,
    NonAvailabilityRoomSerializer,
    LogSerializer,
    WardDataSerializer,
    BudgetYearsSerializer,

)

from .models import (
    Patient,
    Medic,
    NonAvailabilityMedic,
    Operation,
    OperationType,
    Room,
    NonAvailabilityRoom,
    Log,
    WardData,
    BudgetYear,
)


def create_log(http_method: str, user: str, token: str, event_description: str) -> None:
    log = Log(http_method=http_method, user=user, token=token, event_description=event_description)
    log.save()


def retrieve_user(request):
    """
    Retrieves user from database by decoding token from request.

    Args:
        request: HttpRequest

    Returns:
        user: Optional[str] - If couldn't specify the user None is returned, data: dict - Http response header

    Raises:
        ValidationError: If could not decode token
    """
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        user = Account.objects.get(id=user_id)
    except ValidationError as v:
        print("validation error", v)
        return None, data
    return user, data


def allow_access(permissions: List[str]):
    """
    Function decorator to retrieve user (by using retrieve_user()) and ascertain his permissions to view this endpoint

    Args:
        permissions: List[str] List of permission fields in Account model e.g: ['is_admin', 'is_medic']

    Raises:
        ValidationError: If could not decode token
    """

    def allow_access_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            request = args[0]
            user, data = retrieve_user(request)
            if user is None:
                data['failure'] = "Could not specify the user"
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            for p in permissions:
                if user.__dict__.get(p, None) is True:
                    break
            else:
                data['failure'] = "User does not have permissions to view this site"
                data['user'] = str(user)
                return Response(data=data, status=status.HTTP_403_FORBIDDEN)
            kwargs['user'] = user
            kwargs['token'] = data['token']
            return func(*args, **kwargs)

        return func_wrapper

    return allow_access_decorator


# LOGS #
@api_view(['GET', ])
@allow_access(permissions=['is_admin', ])
def view_logs(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    logs = [log for log in Log.objects.all()]
    serializer = LogSerializer(logs, many=True)
    create_log(request.method, user, token, f"Użytkownik {user} wyświetlił liste logów poprzez url api/patients/")
    return Response(serializer.data)


@api_view(['GET', ])
@allow_access(permissions=['is_admin', ])
def view_logs_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        log = Log.objects.get(id=_id)
    except Log.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = LogSerializer(log)
    create_log(request.method, user, token, f"Użytkownik {user} wyświetlił log o id {_id} poprzez url api/patients/")
    return Response(serializer.data)


# Patient Views #
@api_view(['GET', ])
@allow_access(permissions=['is_planist', 'is_ordynator', 'is_medic'])
def all_patients(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    if user.is_medic:
        medic = user.medic
        operations = Operation.objects.filter(medic=medic)
        patients = []
        for operation in operations:
            patients.append(operation.patient)
        patients = list(set(patients))

    else:
        patients = [patient for patient in Patient.objects.all()]

    if request.method == 'GET':
        serializer = PatientSerializer(patients, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił liste pacjentów poprzez url api/patients/")
        return Response(serializer.data)


@api_view(['POST', ])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def create_patient(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył profil pacjenta poprzez url api/create_patient/")
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@allow_access(permissions=['is_planist', 'is_ordynator', 'is_medic'])
def patient_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        patient = Patient.objects.get(id=_id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.is_medic:
        medic = user.medic
        operations = Operation.objects.filter(medic=medic)
        patients = []
        for operation in operations:
            patients.append(operation.patient)
        patients = list(set(patients))
        if patient in patients:
            serializer = PatientSerializer(patient)
            create_log(request.method, user, token,
                       f"Użytkownik {user} zobaczył profil pacjenta o id {id} poprzez url api/patient/<id>/")
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PatientSerializer(patient)
    create_log(request.method, user, token,
               f"Użytkownik {user} zobaczył profil pacjenta o id {id} poprzez url api/patient/<id>/")
    return Response(serializer.data)


@api_view(['PUT'])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def update_patient(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        patient = Patient.objects.get(id=_id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PatientSerializer(patient, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "update successful"
        create_log(request.method, user, token,
                   f"Użytkownik {user} zmienił profil pacjenta o id {_id} poprzez url api/update_patient/<id>/")
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def delete_patient(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        patient = Patient.objects.get(id=_id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = patient.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
            create_log(request.method, user, token,
                       f"Użytkownik {user} usunął profil pacjenta o id {_id} poprzez url api/delete_patient/<id>/")

        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# Medic Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator', ])
def all_medics(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    medics = [medic for medic in Medic.objects.all()]

    if request.method == 'GET':
        serializer = MedicSerializer(medics, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} zobaczył liste lekarzy poprzez url api/medics/")

        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MedicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył profil lekarza poprzez url api/medics/")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Medic.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął {count[0]} lekarzy poprzez url api/medics/")
        return JsonResponse({'message': f'{count[0]} Medics were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def medic_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        medic = Medic.objects.get(id=_id)
    except Medic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicSerializer(medic)
        create_log(request.method, user, token,
                   f"Użytkownik {user} zobaczył lekarza o id {_id} poprzez url api/medic/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MedicSerializer(medic, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował profil lekarza o id {_id} poprzez url api/medic/<id>/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        medic.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął profil lekarza o id {_id} poprzez url api/medic/<id>/")
        return JsonResponse({'message': 'Medic was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Operation Views #
@api_view(['GET'])
@allow_access(permissions=['is_ordynator', 'is_planist', 'is_medic'])
def all_operations(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    if user.is_medic:
        medic = user.medic
        operations = [operation for operation in Operation.objects.filter(medic=medic)]
    else:
        operations = [operation for operation in Operation.objects.all()]

    if request.method == 'GET':
        serializer = OperationSerializer(operations, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} zobaczył liste operacji poprzez url api/operations/")
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def edit_operations(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    if request.method == 'POST':
        room_data = JSONParser().parse(request)
        room_serializer = OperationSerializer(data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył operację poprzez url api/operations/edit/")
            return JsonResponse(room_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Operation.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunał {count[0]} operacji poprzez url api/operations/edit/")
        return JsonResponse({'message': f'{count[0]} Operations were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@allow_access(permissions=['is_ordynator', 'is_planist', 'is_medic'])
def operation_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        operation = Operation.objects.get(id=_id)
    except Operation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user.is_medic:
            if user.medic == operation.medic:
                serializer = OperationSerializer(operation)
                create_log(request.method, user, token,
                           f"Użytkownik {user} wyświetlił operację o id {_id} poprzez url api/operation/<id>/")
                return Response(serializer.data)
            else:
                data = []
                return Response(data=data)
        else:
            serializer = OperationSerializer(operation)
            create_log(request.method, user, token,
                       f"Użytkownik {user} wyświetlił operację o id {_id} poprzez url api/operation/<id>/")
            return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def edit_operation_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        operation = Operation.objects.get(id=_id)
    except Operation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OperationSerializer(operation, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował operację o id {_id} poprzez url api/operation/<id>/edit/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        operation.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął operację o id {_id} poprzez url api/operation/<id>/edit/")
        return JsonResponse({'message': 'Operation was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Room Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_rooms(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    rooms = [room for room in Room.objects.all()]

    if request.method == 'GET':
        serializer = RoomSerializer(rooms, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę pokoi poprzez url api/rooms/")
        return Response(serializer.data)
    elif request.method == 'POST':
        room_data = JSONParser().parse(request)
        room_serializer = RoomSerializer(data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył nową salę poprzez url api/rooms/")
            return JsonResponse(room_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Room.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął {count[0]} sal operacyjnych poprzez url api/rooms/")
        return JsonResponse({'message': f'{count[0]} Rooms were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@allow_access(permissions=['is_ordynator'])
def active_rooms(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    rooms = Room.objects.filter(active=True)

    if request.method == 'GET':
        serializer = RoomSerializer(rooms, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę sal poprzez url api/rooms/active/")
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def room_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        room = Room.objects.get(id=_id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił salę o id {_id} poprzez url api/rooms/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        room_data = JSONParser().parse(request)
        room_serializer = RoomSerializer(room, data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował salę o id {_id} poprzez url api/rooms/<id>/")
            return JsonResponse(room_serializer.data)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        room.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął salę o id {_id} poprzez url api/rooms/<id>/")
        return JsonResponse({'message': 'Room was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Operation_type Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_operation_types(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    operation_types = [operation_type for operation_type in OperationType.objects.all()]

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_types, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę typów operacji poprzez url api/operation_types/")
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OperationTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył typ operacji poprzez url api/operation_types/")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = OperationType.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął {count[0]} typów operacji poprzez url api/operation_types/")
        return JsonResponse({'message': f'{count[0]} operation types were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def operation_type_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        operation_type = OperationType.objects.get(id=_id)
    except OperationType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_type)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił typ operacji o id {_id} poprzez url api/operation_types/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OperationTypeSerializer(operation_type, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował typ operacji o id {_id} poprzez url api/operation_types/<id>/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        operation_type.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunał typ operacji o id {_id} poprzez url api/operation_types/<id>/")
        return JsonResponse({'message': 'NAM was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# NonAvailabilityMedic Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_nams(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    nams = [NAM for NAM in NonAvailabilityMedic.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(nams, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę nieaktywności lekarzy poprzez url api/not_available_medics/")
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityMedicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył nieaktywność lekarza poprzez url api/not_available_medics/")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = NonAvailabilityMedic.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunał {count[0]} nieaktywności lekarzy poprzez url api/not_available_medics/")
        return JsonResponse({'message': f'{count[0]} NAMs were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def nam_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        nam = NonAvailabilityMedic.objects.get(id=_id)
    except NonAvailabilityMedic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(nam)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił nieaktywność lekarza o id {_id} "
                   f"poprzez url api/not_available_medics/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityMedicSerializer(nam, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował nieaktywność lekarza o id {_id} "
                       f"poprzez url api/not_available_medics/<id>/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        nam.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął nieaktywność lekarza o id {_id} "
                   f"poprzez url api/not_available_medics/<id>/")
        return JsonResponse({'message': 'NAM was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# NonAvailabilityRoom Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_nars(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    nars = [NAR for NAR in NonAvailabilityRoom.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(nars, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę nieaktywnych pokoi poprzez url api/not_available_rooms/")
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityRoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzył nieaktywny pokój poprzez url api/not_available_rooms/")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = NonAvailabilityRoom.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął {count[0]} nieaktywnych pokoi poprzez url api/not_available_rooms/")
        return JsonResponse({'message': f'{count[0]} NARs were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def nar_by_id(request, _id, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        nar = NonAvailabilityRoom.objects.get(id=_id)
    except NonAvailabilityRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(nar)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił nieaktywność pokoju o id {_id} "
                   f"poprzez url api/not_available_rooms/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityRoomSerializer(nar, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował nieaktywność pokoju o id {_id} "
                       f"poprzez url api/not_available_rooms/<id>/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        nar.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął nieaktywność pokoju o id {_id} poprzez url api/not_available_rooms/<id>/")
        return JsonResponse({'message': 'NAR was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def budget_years(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    years = [year for year in BudgetYear.objects.all()]

    if request.method == 'GET':
        serializer = BudgetYearsSerializer(years, many=True)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił listę lat budzetowych poprzez url api/budget_years/")
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BudgetYearsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} dodal nowy rok budzetowy poprzez url api/budget_years/")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = BudgetYear.objects.all().delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął {count[0]} lat budzetowych poprzez url api/budget_years/")
        return JsonResponse({'message': f'{count[0]} Budgets were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def budget_year(request, year, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        _budget_year = BudgetYear.objects.get(year=year)
    except BudgetYear.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BudgetYearsSerializer(_budget_year)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił rok {year} poprzez url api/budget_year/<id>/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BudgetYearsSerializer(_budget_year, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} edytował rok {year} poprzez url api/budget_year/<id>/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        _budget_year.delete()
        create_log(request.method, user, token,
                   f"Użytkownik {user} usunął rok {year} poprzez url api/budget_year/<id>/")
        return JsonResponse({'message': 'Year was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@allow_access(permissions=['is_ordynator'])
def create_ward_data(request, *args, **kwargs):
    user = kwargs['user']
    token = kwargs['token']
    try:
        data = JSONParser().parse(request)
        ward_data = WardDataSerializer(data=data)
    except WardData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST' and len(WardData.objects.all()) == 0:
        if ward_data.is_valid():
            ward_data.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} stworzyl nowa konfiguracje poprzez url api/create_ward_data/")
            return JsonResponse(ward_data.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ward_data.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@allow_access(permissions=['is_ordynator'])
def update_ward_data(request, *args, **kwargs):
    data = {}
    user = kwargs['user']
    token = kwargs['token']
    try:
        ward = WardData.objects.all()[0]
    except IndexError:
        data["failure"] = "Please config ward data first"
        return Response(status=status.HTTP_409_CONFLICT, data=data)

    if request.method == 'GET':
        serializer = WardDataSerializer(ward)
        create_log(request.method, user, token,
                   f"Użytkownik {user} wyświetlił konfiguracje poprzez url api/ward_data/")
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data["id"] = ward.id
        serializer = WardDataSerializer(ward, data=data)
        if serializer.is_valid():
            serializer.save()
            create_log(request.method, user, token,
                       f"Użytkownik {user} zaktualizował konfiguracje poprzez url api/ward_data/")
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=data)


@api_view(['GET'])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def statistics(request, *args, **kwargs):
    """

    Args:
        request: GET holding date range for statistics

    Returns:

    """

    user = kwargs['user']
    token = kwargs['token']

    if request.method == 'GET':
        start_year = request.GET.get("start_year")
        start_month = request.GET.get("start_month")
        start_day = request.GET.get("start_day")
        end_year = request.GET.get("end_year")
        end_month = request.GET.get("end_month")
        end_day = request.GET.get("end_day")

        # Check presence of request values
        if start_year is None or start_month is None or start_day is None \
                or end_year is None or end_month is None or end_day is None:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Check is there any operations in range in DB
        start_date = datetime.date(year=int(start_year), month=int(start_month), day=int(start_day))
        end_date = datetime.date(year=int(end_year), month=int(end_month), day=int(end_day))
        operations = Operation.objects.filter(date__range=[start_date, end_date])
        if len(operations) == 0:
            data = {"failure": "There are no operations in DB"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

        try:
            data = get_stats(operations, start_date, end_date)
            result = [data]
            create_log(request.method, user, token,
                       f"Użytkownik {user} wyświetlił statystyki poprzez url api/statistics/")
        except BudgetYear.DoesNotExist:
            data = {"failure": "BudgetYear is empty"}
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data=data)
        return Response(status=status.HTTP_200_OK, data=result)


@api_view(["POST"])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def medic_presence(request, *args, **kwargs):
    """

    Args:
        request: POST request with day and doctorId

    Returns:
        BOOLEAN of doctor presence in particular day

    """

    user = kwargs['user']
    token = kwargs['token']

    if request.method == "POST":
        date_year = request.POST.get("date_year")
        date_month = request.POST.get("date_month")
        date_day = request.POST.get("date_day")
        medic_id = request.POST.get("medic_id")

        if date_year is None or date_month is None or date_day is None or medic_id is None:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            day = datetime.date(year=int(date_year), month=int(date_month), day=int(date_day))
            if checkPresence(day, medic_id) is True:
                create_log(request.method, user, token,
                           f"Użytkownik {user} wyświetlił obecnosc lekarzana z daty {date_year}-{date_month}-{date_day}"
                           f" poprzez url api/medicPresence/")
                return Response(status=status.HTTP_200_OK, data="1")
            else:
                return Response(status=status.HTTP_200_OK, data="0")
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def daily_alg(request, *args, **kwargs):
    """

    Args:
        request: POST request with is_child, is_difficult, year, month, day, type and medic information

    Returns:
        Valid, sorted JSON with data about possible operations

    """
    user = kwargs['user']
    token = kwargs['token']
    data = {}

    if request.method == "POST":
        if len(WardData.objects.all()) == 0:
            data["failure"] = "Please config ward data first"
            return Response(status=status.HTTP_409_CONFLICT, data=data)

        data = JSONParser().parse(request)
        is_child = data["is_child"]  # 1 or 0
        is_difficult = data["is_difficult"]  # 1 or 0
        date_year = data["date_year"]  # int
        date_month = data["date_month"]  # int
        date_day = data["date_day"]  # int
        type_icd = data["type_ICD"]  # int
        medic_id = data["medic_id"]  # int

        # Check presence of request values
        if is_child is None or is_difficult is None or date_year is None \
                or date_month is None or date_day is None or type_icd is None or medic_id is None:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        day_date = datetime.date(year=int(date_year), month=int(date_month), day=int(date_day))
        algorithm = DailyHintALG(int(is_child), int(is_difficult), day_date, type_icd, medic_id)

        json = algorithm.to_json()
        create_log(request.method, user, token,
                   f"Użytkownik {user} zebral dane o mozliwych operacjach poprzez url api/dailyAlg/")

        return Response(status=status.HTTP_200_OK, data=json)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def yearly_alg(request, *args, **kwargs):
    """

    Args:
        request: POST data with

    Returns: JSON with dates and percentage fill of the day

    """
    user = kwargs['user']
    token = kwargs['token']
    data = {}

    if request.method == "POST":
        if len(WardData.objects.all()) == 0:
            data["failure"] = "Please config ward data first"
            return Response(status=status.HTTP_409_CONFLICT, data=data)

        data = JSONParser().parse(request)
        year = data["date_year"]
        month = data["date_month"]

        if year is None:
            data["failure"] = "year is None"
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=data)

        if month is None:
            data["failure"] = "month is None"
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=data)

        if len(Operation.objects.filter(date__year=year)) == 0:
            data["failure"] = "There are no operations in this year"
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)

        if len(Operation.objects.filter(date__month=month)) == 0:
            data["failure"] = "There are no operations in this month"
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)

        json = getPercenteges(year, month)
        create_log(request.method, user, token,
                   f"Użytkownik {user} zebral dane o dniach z operacjami oraz ich zapelnieniu "
                   f"poprzez url api/yearlyAlg/")
        return Response(status=status.HTTP_200_OK, data=json)
