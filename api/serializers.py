from rest_framework import serializers
from .models import (
    Patient,
    Medic,
    NonAvailabilityMedic,
    Operation,
    Operation_type,
    Room,
    NonAvailabilityRoom,
    Log,
)
import re


def code(icd: str) -> bool:
    return bool(re.match(r"^[0-9]{2,3}(\.[0-9]{1,5})?$", icd))


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'PESEL', 'gender', 'age')


class MedicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medic
        fields = ('id', 'name')


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('id', 'type', 'medic', 'patient', 'date', 'room', 'start')


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation_type
        fields = ('id', 'name', 'ICD_code', 'cost', 'is_difficult', 'duration')

    def validate_ICD_code(self, value):
        b = code(str(value))
        if not b:
            raise serializers.ValidationError("given ICD code is not valid")
        return value


class NonAvailabilityMedicSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonAvailabilityMedic
        fields = ('id', 'medic', 'date_start', 'date_end')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'active')


class NonAvailabilityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonAvailabilityRoom
        fields = ('id', 'room', 'date_start', 'date_end')


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('user', 'token', 'event_description', 'time', 'http_method')