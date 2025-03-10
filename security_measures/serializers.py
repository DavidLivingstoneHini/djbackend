from rest_framework import serializers
from.models import GDPRRequest

class GDPRRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDPRRequest
        fields = ['id', 'user', 'request_type', 'created_at']
