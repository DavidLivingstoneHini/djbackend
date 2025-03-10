from django.db import models
from user_auth.models import User


class GDPRRequest(models.Model):
    REQUEST_TYPES = [
        ('ACCESS', 'Access'),
        ('RECTIFICATION', 'Rectification'),
        ('ERASURE', 'Erasure'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
