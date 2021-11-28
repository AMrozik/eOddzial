from rest_framework import serializers
from .models import (
    Patient,
    Medic,
    NonAvailabilityMedic,
    Operation,
    Operation_type,
    Room,
    NonAvailabilityRoom,
)


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


class NonAvailabilityMedicSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonAvailabilityMedic
        fields = ('id', 'medic', 'date_start', 'date_end')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number')


class NonAvailabilityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonAvailabilityRoom
        fields = ('id', 'room', 'date_start', 'date_end')