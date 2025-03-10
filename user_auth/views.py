from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from.serializers import PasswordChangeSerializer
from datetime import timedelta, datetime
from rest_framework_simplejwt.settings import api_settings

from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            expiration_time = datetime.utcnow() + api_settings.ACCESS_TOKEN_LIFETIME
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'expires_in': expiration_time.isoformat() + 'Z',
                "user": UserSerializer(user).data,
                "message": "Registration successful"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            # Calculate expiration time by adding ACCESS_TOKEN_LIFETIME to the current time
            expiration_time = datetime.utcnow() + api_settings.ACCESS_TOKEN_LIFETIME
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'expires_in': expiration_time.isoformat() + 'Z',
                "user": UserSerializer(user).data,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Hello, authenticated user!'}, status=status.HTTP_200_OK)

class RefreshTokenView(TokenViewBase):
    """
    Refresh Token Endpoint
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Simple JWT handles the refresh token logic internally
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)