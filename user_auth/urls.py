from django.urls import path, include
from .views import SignUpView, LoginView, ProfileView, ProtectedView, RefreshTokenView, PasswordChangeView

urlpatterns = [
    path('api/v1/users/signup/', SignUpView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),
    path('api/v1/users/profile/', ProfileView.as_view()),
    path('api/v1/users/protected/', ProtectedView.as_view()),
    path('api/v1/users/token/refresh/', RefreshTokenView.as_view()),
    path('api/v1/users/password/change/', PasswordChangeView.as_view()),
]
