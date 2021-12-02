from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = f"{user.first_name} {user.last_name}"
        token['is_ordynator'] = user.is_ordynator
        token['is_medic'] = user.is_medic
        token['is_planist'] = user.is_planist
        token['is_secretary'] = user.is_secretary
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
