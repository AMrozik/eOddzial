from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import PatientSerializer
from api.models import Patient
from functools import wraps
from rest_framework_simplejwt.backends import TokenBackend
from users.models import Account


def allow_access(permissions):
    def allow_access_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            request = args[0]
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            user = Account.objects.get(id=user_id)
            for p in permissions:
                if user.__dict__[p] is True: break
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return func(*args, **kwargs)
        return func_wrapper
    return allow_access_decorator


# Patient Views #
# GET only
# @allow_access(permissions=['is_admin']) # nope
class PatientsView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# POST only
class CreatePatientsView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# GET only
# function-based view - more customizable i think (or dunno all the options in class-based views)
@api_view(['GET', ])
@allow_access(permissions=['is_admin'])
def patient_by_id(request, id):
    print(request)
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
