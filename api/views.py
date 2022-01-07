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

from api.serializers import (
    PatientSerializer,
    MedicSerializer,
    OperationSerializer,
    OperationTypeSerializer,
    NonAvailabilityMedicSerializer,
    RoomSerializer,
    NonAvailabilityRoomSerializer,
)

from .models import (
    Patient,
    Medic,
    NonAvailabilityMedic,
    Operation,
    Operation_type,
    Room,
    NonAvailabilityRoom,
)


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
                if user.__dict__.get(p, None) is True: break
            else:
                data['failure'] = "User does not have permissions to view this site"
                data['user'] = str(user)
                return Response(data=data, status=status.HTTP_403_FORBIDDEN)
            kwargs['user'] = user
            return func(*args, **kwargs)
        return func_wrapper
    return allow_access_decorator


# Patient Views #
@api_view(['GET', ])
@allow_access(permissions=['is_planist', 'is_ordynator', 'is_medic'])
def all_patients(request, *args, **kwargs):
    user = kwargs['user']
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
        return Response(serializer.data)


@api_view(['POST', ])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def create_patient(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@allow_access(permissions=['is_planist', 'is_ordynator', 'is_medic'])
def patient_by_id(request, id, *args, **kwargs):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = kwargs['user']
    if user.is_medic:
        medic = user.medic
        operations = Operation.objects.filter(medic=medic)
        patients = []
        for operation in operations:
            patients.append(operation.patient)
        patients = list(set(patients))
        if patient in patients:
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PatientSerializer(patient)
    return Response(serializer.data)


@api_view(['PUT'])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def update_patient(request, id, *args, **kwargs):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PatientSerializer(patient, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "update successful"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@allow_access(permissions=['is_planist', 'is_ordynator'])
def delete_patient(request, id, *args, **kwargs):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = patient.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# Medic Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator', ])
def all_medics(request, *args, **kwargs):
    medics = [medic for medic in Medic.objects.all()]

    if request.method == 'GET':
        serializer = MedicSerializer(medics, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MedicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Medic.objects.all().delete()
        return JsonResponse({'message': '{} Medics were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def medic_by_id(request, id, *args, **kwargs):
    try:
        medic = Medic.objects.get(id=id)
    except Medic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicSerializer(medic)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MedicSerializer(medic, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        medic.delete()
        return JsonResponse({'message': 'Medic was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Operation Views #
@api_view(['GET'])
@allow_access(permissions=['is_ordynator', 'is_planist', 'is_medic'])
def all_operations(request, *args, **kwargs):
    user = kwargs['user']
    if user.is_medic:
        medic = user.medic
        operations = [operation for operation in Operation.objects.filter(medic=medic)]
    else:
        operations = [operation for operation in Operation.objects.all()]

    if request.method == 'GET':
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def edit_operations(request, *args, **kwargs):
    if request.method == 'POST':
        room_data = JSONParser().parse(request)
        room_serializer = OperationSerializer(data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            return JsonResponse(room_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Operation.objects.all().delete()
        return JsonResponse({'message': '{} Operations were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@allow_access(permissions=['is_ordynator', 'is_planist', 'is_medic'])
def operation_by_id(request, id, *args, **kwargs):
    user = kwargs['user']
    try:
        operation = Operation.objects.get(id=id)
    except Operation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user.is_medic:
            if user.medic == operation.medic:
                serializer = OperationSerializer(operation)
                return Response(serializer.data)
            else:
                data = []
                return Response(data=data)
        else:
            serializer = OperationSerializer(operation)
            return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def edit_operation_by_id(request, id, *args, **kwargs):
    try:
        operation = Operation.objects.get(id=id)
    except Operation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OperationSerializer(operation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        operation.delete()
        return JsonResponse({'message': 'Operation was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Room Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_rooms(request, *args, **kwargs):
    rooms = [room for room in Room.objects.all()]

    if request.method == 'GET':
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        room_data = JSONParser().parse(request)
        room_serializer = RoomSerializer(data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            return JsonResponse(room_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Room.objects.all().delete()
        return JsonResponse({'message': '{} Rooms were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@allow_access(permissions=['is_ordynator'])
def active_rooms(request, *args, **kwargs):
    rooms = Room.objects.filter(active=True)

    if request.method == 'GET':
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def room_by_id(request, id, *args, **kwargs):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    elif request.method == 'PUT':
        room_data = JSONParser().parse(request)
        room_serializer = RoomSerializer(room, data=room_data)
        if room_serializer.is_valid():
            room_serializer.save()
            return JsonResponse(room_serializer.data)
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        room.delete()
        return JsonResponse({'message': 'Room was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# Operation_type Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_operation_types(request, *args, **kwargs):
    operation_types = [operation_type for operation_type in Operation_type.objects.all()]

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_types, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OperationTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Operation_type.objects.all().delete()
        return JsonResponse({'message': '{} operation types were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def operation_type_by_id(request, id, *args, **kwargs):
    try:
        operation_type = Operation_type.objects.get(id=id)
    except Operation_type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_type)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OperationTypeSerializer(operation_type, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        operation_type.delete()
        return JsonResponse({'message': 'NAM was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# NonAvailabilityMedic Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_NAMs(request, *args, **kwargs):
    NAMs = [NAM for NAM in NonAvailabilityMedic.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(NAMs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityMedicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = NonAvailabilityMedic.objects.all().delete()
        return JsonResponse({'message': '{} NAMs were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def NAM_by_id(request, id, *args, **kwargs):
    try:
        NAM = NonAvailabilityMedic.objects.get(id=id)
    except NonAvailabilityMedic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(NAM)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityMedicSerializer(NAM, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        NAM.delete()
        return JsonResponse({'message': 'NAM was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# NonAvailabilityRoom Views #
@api_view(['GET', 'POST', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def all_NARs(request, *args, **kwargs):
    NARs = [NAR for NAR in NonAvailabilityRoom.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(NARs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityRoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = NonAvailabilityRoom.objects.all().delete()
        return JsonResponse({'message': '{} Rooms were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@allow_access(permissions=['is_ordynator'])
def NAR_by_id(request, id, *args, **kwargs):
    try:
        NAR = NonAvailabilityRoom.objects.get(id=id)
    except NonAvailabilityRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(NAR)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NonAvailabilityRoomSerializer(NAR, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        NAR.delete()
        return JsonResponse({'message': 'NAR was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@allow_access(permissions=['is_ordynator', 'is_planist'])
def dailyAlg(request, *args, **kwargs):
    """

    Args:
        request: POST request with isChild, isDifficult, year, month, day, type and medic information

    Returns:
        Valid, sorted JSON with data about possible operations

    """
    if request.method == "POST":
        is_child = request.POST.get("is_child")             # 1 or 0
        is_difficult = request.POST.get("is_difficult")     # 1 or 0
        date_year = request.POST.get("date_year")           # int
        date_month = request.POST.get("date_month")         # int
        date_day = request.POST.get("date_day")             # int
        type_ICD = request.POST.get("type_ICD")             # int
        medic_id = request.POST.get("medic_id")             # int

        if is_child is None or is_difficult is None or date_year is None or date_month is None or date_day is None or type_ICD is None or medic_id is None:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            day_date = datetime.date(year=int(date_year), month=int(date_month), day=int(date_day))
            algorithm = DailyHintALG(int(is_child), int(is_difficult), day_date, type_ICD, medic_id)

            json = algorithm.toJSON()

            return Response(status=status.HTTP_200_OK, data=json)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)