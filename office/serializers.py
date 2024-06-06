from django.db import transaction

from rest_framework import serializers
from .models import Office, BankAccounts, Company, CompanyRole
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

            # Create bank accounts for the office without saving to the database
            bank_accounts_instances = []
            for bank_account_data in bank_accounts_data:
                bank_account_instance = BankAccounts.objects.create(Office=office, **bank_account_data)
                bank_accounts_instances.append(bank_account_instance)

            # Create invite employee objects without saving to the database
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