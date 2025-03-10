from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'health_profile', 'date_of_birth', 'gender', 'password', 'is_staff', 'is_superuser', 'created_at',
            'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data.get('is_superuser') and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("Only superusers can create new superusers")
        if data.get('is_staff') and not (
                self.context['request'].user.is_superuser or self.context['request'].user.is_staff):
            raise serializers.ValidationError("Only superusers and staff can create new staff")
        return data

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        is_superuser = validated_data.pop('is_superuser', False)
        user = User.objects.create_user(**validated_data)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already in use')
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'health_profile', 'date_of_birth', 'gender', 'is_staff', 'is_superuser', 'created_at',
            'updated_at']
        read_only_fields = ['is_superuser', 'is_staff']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError({
                'email': ['Invalid email or password. Please try again.']
            })

        # Return the actual user object
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
