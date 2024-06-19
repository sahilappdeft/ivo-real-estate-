from django.db import transaction
from django.contrib.auth.models import Permission

from rest_framework import serializers
from .models import (Office, BankAccounts, Company, CompanyRole,
                     OfficeUnit, OfficeEmployee)
from employee.serializers import InviteEmployeeSerializer, EmployeeSerializer
from employee.models import InviteEmployee, Employee

  
class OfficeSerializer(serializers.ModelSerializer):
    office_unit = serializers.CharField(source='office_units.first.name', read_only=True)
    employee =  serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Office
        exclude = ['company', 'user']
        extra_kwargs = {
            'user': {'read_only': True},
            'company': {'read_only': True}
        }
        
    def get_employee(self, instance):
        return instance.office_employee.all().count()
     
    
class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['purpose', 'owner_name', 'iban', 'bic']


class OfficeEmployeeSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = OfficeEmployee
        fields = ['office', 'employee', 'position']


class GetOfficeEmployeeSeriliazer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    class Meta:
        model = OfficeEmployee
        fields = ['id', 'office', 'employee', 'position']

    def get_employee(self, instance):
        data = {
            'id': instance.employee.id,
            'employee_id': instance.employee.employee_id,
            'role': instance.employee.role.name
        }
        return data


class OfficeAndBankAccountsSerializer(serializers.Serializer):
    office = OfficeSerializer()
    bank_accounts = BankAccountsSerializer(many=True)
    invite_employee = InviteEmployeeSerializer(many=True)
    add_employee = OfficeEmployeeSeriliazer(required=False, many=True)
    
    def create(self, validated_data):
        office_data = validated_data.pop('office')
        bank_accounts_data = validated_data.pop('bank_accounts')
        invite_employees_data = validated_data.pop('invite_employee')
        add_employees_data = validated_data.pop('add_employee', [])
        
        # get request user
        user = self.context['request'].user
        company = None
        
        try:
            company = user.employee.company
        except Company.DoesNotExist:
            company = None
        try:
            with transaction.atomic():
                if not company:
                    company = Company.objects.create(user=user)
                    # get admin role of company
                    role = CompanyRole.objects.get(name='admin')
                    # creae employe object for admin
                    employee = Employee.objects.create(company=company,user=user,
                                        role=role)
            
                # Create office object without saving to the database
                office = Office.objects.create(user=user, company=company, **office_data)

                # Create bank accounts for the office 
                for bank_account_data in bank_accounts_data:
                    bank_account_instance = BankAccounts.objects.create(office=office, **bank_account_data)

                # Create invite employee objects
                for invite_employee_data in invite_employees_data:
                    invite_employee_instance = InviteEmployee.objects.create(sender=office, **invite_employee_data)
                    
                # Assign existing empoyee to office
                for add_employee_data in  add_employees_data:
                    try:
                        # if employee already in office by pass
                        add_employee_instance = OfficeEmployee.objects.create(Office=office, **add_employee_data) 
                    except:
                        pass
        except Exception as e:
            print(e)
            
            return serializers.ValidationError("Failed to create office, bank accounts, or invite employees")

        return {
                'office': OfficeSerializer(office).data,
                }


class CompanyRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyRole
        fields = '__all__'
        
    def create(self, validated_data):
        data = validated_data

        # get request user
        user = self.context['request'].user
        company = None
        # if user.role == "company":
        #     company = user.company_user
        # elif user.role == "employee":
        #     company = user.office.company
        company = user.employee.company
        try:
            with transaction.atomic():
                # Create company role object 
                company_role = CompanyRole.objects.create(company=company, name=data['name'])

                # Assign permissions to role
                permissions = data['permission']
                for codename in permissions:
                    try:
                        #By pass the permmison if permission not founds
                        permission = Permission.objects.get(codename=codename)
                        company_role.permission.add(permission)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            return serializers.ValidationError("Failed to create company role")

        return company_role
    
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        permissions = validated_data.get('permission', [])

        # Clear existing permissions
        instance.permission.clear()

        # Add new permissions
        for codename in permissions:
            try: 
                #By pass the permmison if permission not found
                permission = Permission.objects.get(codename=codename)
                instance.permission.add(permission)
            except Exception as e:
                print(e)
        # Save the updated instance
        instance.save()

        return instance
    
    
class DetailCompanyRoleSerializer(serializers.ModelSerializer):
    employees =serializers.SerializerMethodField()
    
    class Meta:
        model = CompanyRole
        fields = '__all__'

    def get_employees(self, instance):
        return Employee.objects.filter(role=instance)


class OfficeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeUnit
        fields = '__all__'
        
        
        
class DetailedOfficeSerializer(serializers.ModelSerializer):
    bank_accounts = serializers.SerializerMethodField()
    employees = serializers.SerializerMethodField()
    
    class Meta:
        model = Office
        exclude = ['company', 'user',]

    def get_bank_accounts(self, instance):
        bank_accounts = instance.offic_banks.all()
        if bank_accounts.exists():
            return BankAccountsSerializer(bank_accounts, many=True).data
        return []

    def get_employees(self, instance):
        employees = instance.office_employee.all()
        if employees.exists():
            return GetOfficeEmployeeSeriliazer(employees, many=True).data
        return []