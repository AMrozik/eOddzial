from rest_framework import serializers
from .models import Account


class AccountSerializes(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'medic', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist']
