from rest_framework import serializers
from .models import InviteEmployee, Employee


class InviteEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmployee
        fields = ['recipient_email', 'role']
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'role']