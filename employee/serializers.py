from rest_framework import serializers
from .models import InviteEmployee


class InviteEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmployee
        fields = ['recipient_email', 'role']