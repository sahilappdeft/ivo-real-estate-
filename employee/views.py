from django.shortcuts import render
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from auth_user.permission import IsTokenValid, token_required
from .models import Employee
from .serializers import EmployeeSerializer
# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the employee.
    '''
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = (IsTokenValid,)
    
    def get_queryset(self):
        
        user=self.request.user
        # if user.role == "company":
        #     company = user.company_user
        # elif user.role == "employee":
        #     company = user.office.company
        
        company = user.employee_company.company
        return Employee.objects.filter(company=company)
    
    def destroy(self, request, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,  request):
        pass