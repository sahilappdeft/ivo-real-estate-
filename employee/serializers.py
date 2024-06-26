from rest_framework import serializers
from .models import InviteEmployee, Employee


class InviteEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmployee
        fields = ['recipient_email', 'role']
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        exclude = ['company']
        depth = 1
        

class DetailEmployeeSerializer(serializers.ModelSerializer):
    
    offices = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        exclude = ['company']
        depth = 1
    
    def get_offices(self, instance):
        
        offices = instance.employee_office.all()
        for office in offices:
            if office:
                return {
                    "id": office.office.id,
                    "name":office.office.name,
                    "position":office.position
                    }
        return []