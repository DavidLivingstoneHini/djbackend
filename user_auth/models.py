from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError


def validate_health_profile(value):
    expected_structure = {
        'height': int,
        'weight': int,
        'allergies': list
    }
    for key, expected_type in expected_structure.items():
        if key not in value or not isinstance(value[key], expected_type):
            raise ValidationError(f'Invalid health profile structure. Expected {key} to be of type {expected_type.__name__}')


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=False, null=False, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z\s\-\' ]{2,50}$',
            message='Full name contains invalid characters. Please use only letters, spaces, hyphen, and apostrophe.'
        )
    ])
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    health_profile = models.JSONField(null=True, blank=True, validators=[validate_health_profile])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'user_auth'

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='%(app_label)s_%(class)s_groups',
        related_query_name='%(app_label)s_%(class)s',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='%(app_label)s_%(class)s_permissions',
        related_query_name='%(app_label)s_%(class)s',
        blank=True,
    )
