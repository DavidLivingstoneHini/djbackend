import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from.models import User
from.serializers import RegisterSerializer, UserSerializer, LoginSerializer

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            full_name='Test User',
            phone_number='+1234567890',
            health_profile={'key': 'value'}
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.phone_number, '+1234567890')
        self.assertEqual(self.user.health_profile, {'key': 'value'})

    def test_user_update(self):
        self.user.full_name = 'Updated Test User'
        self.user.save()
        self.assertEqual(self.user.full_name, 'Updated Test User')

    def test_user_deletion(self):
        self.user.delete()
        self.assertEqual(User.objects.filter(email='test@example.com').exists(), False)


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            full_name='Test User',
            phone_number='+1234567890',
            health_profile={'key': 'value'}
        )

    def test_register_serializer(self):
        data = {
            'email': 'new@example.com',
            'full_name': 'New Test User',
            'phone_number': '+9876543210',
            # 'health_profile': {'new_key': 'new_value'},
            'password': 'strong_password'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data['email'], 'test@example.com')
        self.assertEqual(serializer.data['full_name'], 'Test User')
        self.assertEqual(serializer.data['phone_number'], '+1234567890')
        self.assertEqual(serializer.data['health_profile'], {'key': 'value'})

    def test_login_serializer(self):
        data = {'email': 'test@example.com', 'password': 'password'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='test@example.com',
            full_name='Test User',
            phone_number='+1234567890',
            health_profile={'key': 'value'}
        )

    def test_signup_view(self):
        url = reverse('signup')
        data = {
            'email': 'new@example.com',
            'full_name': 'New Test User',
            'phone_number': '+9876543210',
            'health_profile': {'new_key': 'new_value'},
            'password': 'strong_password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_login_view(self):
        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        url = reverse('profile')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['full_name'], 'Test User')
        self.assertEqual(response.data['phone_number'], '+1234567890')
        self.assertEqual(response.data['health_profile'], {'key': 'value'})

    def test_protected_view(self):
        url = reverse('protected')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Hello, authenticated user!')


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='test@example.com',
            full_name='Test User',
            phone_number='+1234567890',
            health_profile={'key': 'value'}
        )

    def test_token_refresh(self):
        url = reverse('token_refresh')
        # Assuming you have a RefreshToken utility
        refresh_token = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh_token)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_token_authentication(self):
        url = reverse('protected')
        # Assuming you have an AccessToken utility
        access_token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Hello, authenticated user!')

