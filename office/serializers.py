from django.db import transaction

from rest_framework import serializers
from .models import Office, BankAccounts, Company, CompanyRole, RolePermissiom
from employee.serializers import InviteEmployeeSerializer
from employee.models import InviteEmployee

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        exclude = ['company', 'user']


class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['purpose', 'owner_name', 'iban', 'bic']



class OfficeAndBankAccountsSerializer(serializers.Serializer):
    office = OfficeSerializer()
    bank_accounts = BankAccountsSerializer(many=True)
    invite_employee = InviteEmployeeSerializer(many=True)

    def create(self, validated_data):
        office_data = validated_data.pop('office')
        bank_accounts_data = validated_data.pop('bank_accounts')
        invite_employees_data = validated_data.pop('invite_employee')

        # get request user
        user = self.context['request'].user
        company = None
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
            
        with transaction.atomic():
            # Create office object without saving to the database
            office = Office.objects.create(user=user, company=company, **office_data)

            # Create bank accounts for the office 
            bank_accounts_instances = []
            for bank_account_data in bank_accounts_data:
                bank_account_instance = BankAccounts.objects.create(Office=office, **bank_account_data)
                bank_accounts_instances.append(bank_account_instance)

            # Create invite employee objects
            invite_employee_instances = []
            for invite_employee_data in invite_employees_data:
                invite_employee_instance = InviteEmployee.objects.create(sender=office, **invite_employee_data)
                invite_employee_instances.append(invite_employee_instance)
                
            # # save office instace
            # office = office.save()
            # # save  BankAccounts
            # bank_accounts = BankAccounts.objects.bulk_create(bank_accounts_instances)
            # #save invite employee
            # invite_employee = InviteEmployee.objects.bulk_create(invite_employee_instances)

        return {
            'office': OfficeSerializer(office).data,
            'bank_accounts': BankAccountsSerializer(bank_accounts_instances, many=True).data,
            'invite_employee': InviteEmployeeSerializer(invite_employee_instances, many=True).data
        }

class RolePermissiomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermissiom
        fields = '__all__'


class CompanyRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyRole
        fields = '__all__'
        
        
class CompanyRolePermissionSerializer(serializers.Serializer):
    Company_role = CompanyRoleSerializer()
    permissions = RolePermissiomSerializer(many=True)
    
    def create(self, validated_data):
        Company_role_data = validated_data.pop('Company_role')
        permissions_data = validated_data.pop('permissions')

        # get request user
        user = self.context['request'].user
        company = None
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
            
        with transaction.atomic():
            # Create company role object 
            company_role = CompanyRole.objects.create(company=company, **Company_role_data)
            
            # Create permissiona  for the role 
            permissions_imstances = []
            for permission in permissions_data:
                permission_instance = RolePermissiom.objects.create(company=company, 
                                                                    role=company_role,
                                                                    **permission
                                                                )
                permissions_imstances.append(permission_instance)
                
        return {
            'role': CompanyRoleSerializer(company_role).data,
            'permissions': RolePermissiomSerializer(permissions_imstances, many=True).data,
        }