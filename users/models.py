from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from api.models import Medic


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        if user.is_medic is True and user.medic is None:
            raise ValueError("Medic permissions was set to true but didn't provided any medic data")

        if user.medic is not None:
            user.is_medic = True

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('medic', None)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=80, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # have to be here dont ask questions
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    is_ordynator = models.BooleanField(default=False)
    is_medic = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_planist = models.BooleanField(default=False)

    medic = models.OneToOneField(Medic, on_delete=models.PROTECT, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
