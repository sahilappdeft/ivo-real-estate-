from django.db import transaction

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import models

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action

from utility.helpers import success, error
from auth_user.permission import IsTokenValid, token_required
from .models import Office, CompanyRole, OfficeUnit, Company, BankAccounts
from .serializers import (OfficeSerializer, OfficeAndBankAccountsSerializer,
                          CompanyRoleSerializer, OfficeUnitSerializer, OfficeSerializer,
                          DetailedOfficeSerializer, DetailCompanyRoleSerializer
                        )
from .filters import OfficeFilter

class OfficeApiView(viewsets.ModelViewSet):
    '''
    This class provide the crud of the Office.
    '''
    serializer_class = OfficeSerializer
    permission_classes = (IsTokenValid,)
    filterset_class = OfficeFilter

    def get_queryset(self):
        queryset = Office.objects.all()
        employee_count = self.request.query_params.get('employee_count', None)
        if employee_count:
            # Filter based on the count of related employees
            queryset = queryset.annotate(num_employees=models.Count('office_employee')).filter(num_employees=employee_count)
        return queryset

    # @action(detail=False, methods=['get'])
    # @token_required  # assuming you have a token_required decorator
    def list(self, request, *args, **kwargs):
          
        company_id = kwargs.get('company')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(error('Company not found', {}), status=status.HTTP_404_NOT_FOUND)
        
        # Filter offices based on the company
        offices = self.get_queryset().filter(company=company)
        serializer = OfficeSerializer(offices, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        # Add request to serializer context
        serializer.context['request'] = request
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedOfficeSerializer(instance)
        return Response(serializer.data)
    
    # def update(self, request, *args, **kwargs):
        
    #     instance = self.get_object()
    #     data = request.data.copy()
    #     serializer = OfficeAndBankAccountsSerializer(instance, data=request.data)
    #     bank_accounts_data = data.pop('bank_accounts', [])
    #     add_employees_data = data.pop('add_employee', [])
    #     if serializer.is_valid():
    #         try:
    #             with transaction.atomic():
    #                 data = serializer.save()

    #                 # Update or create rooms for the building unit
    #                 for bank_account_data in bank_accounts_data:
    #                     room_id = bank_account_data.pop('id', None)
    #                     is_delete = bank_account_data.pop('is_delete', False)
    #                     if room_id and not is_delete:
    #                         room_instance, created = Room.objects.update_or_create(
    #                             id=room_id,
    #                             defaults={**bank_account_data, 'building_unit': instance}
    #                         )
    #                     elif is_delete:
    #                         Room.objects.get(id=room_id).soft_delete()
    #                     else:
    #                         Room.objects.create(building_unit=instance, **bank_account_data)

    #                 # Update or create energy meters for the building unit
    #                 for add_employee_data in add_employees_data:
    #                     energy_meter_id = add_employee_data.pop('id', None)
    #                     is_delete = add_employee_data.pop('is_delete', False)
    #                     if energy_meter_id and not is_delete:
    #                         energy_meter_instance, created = EnergyMeter.objects.update_or_create(
    #                             id=energy_meter_id,
    #                             defaults={**add_employee_data, 'building_unit': instance}
    #                         )
    #                     elif is_delete:
    #                         EnergyMeter.objects.get(id=energy_meter_id,).soft_delete()
    #                     else:
    #                         EnergyMeter.objects.create(building_unit=instance, **add_employee_data)
                            
    #                 return Response(data, status=status.HTTP_201_CREATED)
    #         except Room.DoesNotExist:
    #             return Response("Room id not found", status=status.HTTP_400_BAD_REQUEST)
    #         except EnergyMeter.DoesNotExist:
    #             return Response("Energy id not found", status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #             print(e)
    #             return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CompanyRoleViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the compnay role.
    '''
    serializer_class = CompanyRoleSerializer
    queryset = CompanyRole.objects.all()
    permission_classes = (IsTokenValid,)

    def list(self, request, *args, **kwargs):
        
        company_id = kwargs.get('company')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(error('Company not found', {}), status=status.HTTP_404_NOT_FOUND)
            
        # Get all CompanyRole objects   
        company_roles = CompanyRole.objects.filter(company=company)
        
        # Serialize the data
        serializer = self.serializer_class(company_roles, many=True)
        
        # Return serialized data with status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, company=None, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except CompanyRole.DoesNotExist:
            return Response({"error": "Company role not found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailCompanyRoleSerializer(instance)
        return Response(serializer.data)


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