from django.urls import path
from.views import GDPRRequestView, UserDataView, UserDataErasureView

urlpatterns = [
    path('gdpr/request/', GDPRRequestView.as_view()),
    path('gdpr/data/', UserDataView.as_view()),
    path('gdpr/erase/', UserDataErasureView.as_view()),
]
