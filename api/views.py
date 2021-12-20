from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from functools import wraps
from rest_framework_simplejwt.backends import TokenBackend
from users.models import Account
from django.core.exceptions import ValidationError
from typing import List


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
            return func(*args, **kwargs)
        return func_wrapper
    return allow_access_decorator


# Patient Views #
@api_view(['GET', ])
@allow_access(permissions=['is_admin'])
def all_patients(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


@api_view(['POST', ])
@allow_access(permissions=['is_admin'])
def create_patient(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@allow_access(permissions=['is_admin'])
def patient_by_id(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


@api_view(['PUT', ])
def update_patient(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def delete_patient(request, id):
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
@api_view(['GET', ])
def medic_by_id(request, id):
    try:
        medic = Medic.objects.get(id=id)
    except Medic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicSerializer(medic)
        return Response(serializer.data)


@api_view(['GET', ])
def all_medics(request):
    medics = [medic for medic in Medic.objects.all()]

    if request.method == 'GET':
        serializer = MedicSerializer(medics, many=True)
        return Response(serializer.data)


# Operation Views #
@api_view(['GET', ])
def all_operations(request):
    operations = [operation for operation in Operation.objects.all()]

    if request.method == 'GET':
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def operation_by_id(request, id):
    try:
        operation = Operation.objects.get(id=id)
    except Medic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OperationSerializer(operation)
        return Response(serializer.data)


# Room Views #
@api_view(['GET', 'POST', 'DELETE'])
def all_rooms(request):
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


# Nie działa, problem z migracją
@api_view(['GET'])
def active_rooms(request):
    rooms = Room.objects.filter(active=True)

    if request.method == 'GET':
        serializer = RoomSerializer(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def room_by_id(request, id):
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
@api_view(['GET', ])
def all_operation_types(request):
    operation_types = [operation_type for operation_type in Operation_type.objects.all()]

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_types, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def operation_type_by_id(request, id):
    try:
        operation_type = Operation_type.objects.get(id=id)
    except Operation_type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OperationTypeSerializer(operation_type)
        return Response(serializer.data)


# NonAvailabilityMedic Views #
@api_view(['GET', ])
def all_NAMs(request):
    NAMs = [NAM for NAM in NonAvailabilityMedic.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(NAMs, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def NAM_by_id(request, id):
    try:
        NAM = NonAvailabilityMedic.objects.get(id=id)
    except NAM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityMedicSerializer(NAM)
        return Response(serializer.data)


# NonAvailabilityRoom Views #
@api_view(['GET', ])
def all_NARs(request):
    NARs = [NAR for NAR in NonAvailabilityRoom.objects.all()]

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(NARs, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def NAR_by_id(request, id):
    try:
        NAR = NonAvailabilityRoom.objects.get(id=id)
    except NAR.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NonAvailabilityRoomSerializer(NAR)
        return Response(serializer.data)