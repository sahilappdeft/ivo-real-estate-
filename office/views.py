from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from django.db import models

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action

from auth_user.permission import IsTokenValid, token_required
from .models import Office, CompanyRole, OfficeUnit
from .serializers import (OfficeSerializer, OfficeAndBankAccountsSerializer,
                          CompanyRoleSerializer, OfficeUnitSerializer, OfficeSerializer
                        )


class OfficeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    
    class Meta:
        model = Office
        fields = ['name', 'address', 'office_units', 'office_rep']

class OfficeApiView(viewsets.ModelViewSet):
    serializer_class = OfficeSerializer
    # permission_classes = (IsTokenValid,)
    filterset_class = OfficeFilter

    def get_queryset(self):
        queryset = Office.objects.all()
        employee_count = self.request.query_params.get('employee_count', None)
        print(employee_count, "employee_count")
        print(queryset, "queryset")
        if employee_count:
            # Filter based on the count of related employees
            queryset = queryset.annotate(num_employees=models.Count('office_employee')).filter(num_employees=employee_count)
        return queryset

    def list(self, request, *args, **kwargs):
        print(self.get_queryset(),"::455454::")
        return super().list(request, *args, **kwargs)
    # def list(self, request):
    #     # Render the HTML template for office register  
    #     return render(request, 'office-register.html')
    
    @action(detail=False, methods=['get'])
    # @token_required  # assuming you have a token_required decorator
    def office_list(self, request):
        
        user = request.user
        # Check the user's role to determine the company
        # if user.role == "company":
        #     company = user.company_user
        # elif user.role == "employee":
        #     company = user.office.company
        company = user.employee_company.company
        
        # Filter offices based on the company
        offices = Office.objects.filter(company=company)
        serializer = OfficeSerializer(offices, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    @method_decorator(token_required)
    def create(self, request):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        # Add request to serializer context
        serializer.context['request'] = request
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CompanyRoleViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the compnay role.
    '''
    serializer_class = CompanyRoleSerializer
    queryset = CompanyRole.objects.all()

    @method_decorator(token_required)
    def list(self, request):
        
        user=request.user
        # if user.role == "company":
        #     company = user.company_user
        # elif user.role == "employee":
        #     company = user.office.company
        company = user.employee_company.company
            
        # Get all CompanyRole objects   
        company_roles = CompanyRole.objects.filter(company=company)
        
        # Serialize the data
        serializer = self.serializer_class(company_roles, many=True)
        
        # Return serialized data with status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except CompanyRole.DoesNotExist:
            return Response({"error": "Company role not found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    

class OfficeUnitViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the office unit.
    '''
    queryset = OfficeUnit.objects.all()
    serializer_class = OfficeUnitSerializer
    # permission_classes = (IsTokenValid,)
    
    def destroy(self, request, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except OfficeUnit.DoesNotExist:
            return Response({"error": "Office unit not found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)