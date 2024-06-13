from django.db import transaction
from django.contrib.auth.models import Permission

from rest_framework import serializers
from .models import Office, BankAccounts, Company, CompanyRole, OfficeUnit
from employee.serializers import InviteEmployeeSerializer
from employee.models import InviteEmployee

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        # exclude = ['company', 'user']
        extra_kwargs = {
            'user': {'read_only': True},
            'company': {'read_only': True}
        }

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


class CompanyRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyRole
        fields = '__all__'
        

    def create(self, validated_data):
        data = validated_data

        # get request user
        user = self.context['request'].user
        company = None
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
        
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
    

class OfficeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeUnit
        fields = '__all__'