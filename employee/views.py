from django.shortcuts import render
from django.db import transaction
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from utility.helpers import success, error, generateOTP
from utility.fast_api import call_auth_microservice
from utility.emailTemplates import send_mail

from auth_user.models import CustomUser
from office.models import OfficeEmployee, CompanyRole, Office, Company
from auth_user.permission import IsTokenValid, token_required
from .models import Employee
from .serializers import EmployeeSerializer, DetailEmployeeSerializer
# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the employee.
    '''
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsTokenValid,)
    
    def get_queryset(self, request, *args, **kwargs):
        
        company_id = kwargs.get('company')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(error('Company not found', {}), status=status.HTTP_404_NOT_FOUND)
        
        return Employee.objects.filter(company=company)
    
    def destroy(self, request, company=None, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailEmployeeSerializer(instance)
        return Response(serializer.data)
    
    def create(self,  request):
        
        data = request.data.copy()
        role = data.pop('role')
        employee_id = data.pop('employee_id')
        offices = data.pop('offices')
        # Get company
        user=self.request.user
        company = user.employee_company.company
        
        if not 'first_name' in data and not 'last_name' in data:
            # Name is required
            return Response(error("First Name and Last Name is required", {}),
                            status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            # Email is required
            return Response(error("Email is required", {}), status=status.HTTP_400_BAD_REQUEST)
        
        # create default password for user
        password = generateOTP()
        data['password'] = password  #add password in data

        #hit request to auth microservice
        response = call_auth_microservice('/signup', data)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            user_id = response_data.get('id')
            email = response_data.get('email')
            first_name = response_data.get('first_name')
            last_name = response_data.get('last_name')

            try:
                with transaction.atomic():
                    #create user wih response User-ID.
                    user = CustomUser.objects.create(user_id=user_id, email=email,
                                                    first_name=first_name, last_name=last_name,)
                    
                    # Get Role
                    try:
                        role_instance = CompanyRole.objects.get(id=role, company=company)
                    except:
                        return response(error('Role with this id does not exist', {}),
                                        status=status.HTTP_404_NOT_FOUND)
                    # create employee
                    employee = Employee.objects.create(role=role_instance, employee_id=employee_id, user=user,
                                            company=company)
                    
                    # Get office
                    try:
                        for office in offices:
                            office_instance = Office.objects.get(id=office['id'])
                            
                            # Assign employe to office
                            office_employe = OfficeEmployee.objects.create(employee=employee, 
                                                                   office=office_instance,
                                                                   position=office['position']
                                                                )
                    except:
                        return response(error('Office with this id does not exist', {}),
                                        status=status.HTTP_404_NOT_FOUND)
                    
                    # send mail with credentials
                    '''subject="Employee Invitation"
                    template = "dd"
                    context = {"email":email, "password":password}
                    send_mail(subject, email, context, template)'''
                    
                    # Registration Successful
                    return Response({"message": "Employee Added Successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response(error('Somethinh went wrong while create employee', {}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return error from the authentication microservice
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)
        