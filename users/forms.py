from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account, MyAccountManager


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        objects = MyAccountManager()
        fields = ('email', 'first_name', 'last_name', 'medic', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Account
        objects = MyAccountManager()
        fields = ('email', 'first_name', 'last_name', 'medic', 'is_ordynator', 'is_medic', 'is_secretary', 'is_planist')
