from rest_framework import serializers
from .models import Office, BankAccounts

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'


class OfficeAndBankAccountsSerializer(serializers.Serializer):
    office = OfficeSerializer()
    bank_accounts = BankAccountsSerializer(many=True)

    def create(self, validated_data):
        office_data = validated_data.pop('office')
        bank_accounts_data = validated_data.pop('bank_accounts')

        office = Office.objects.create(**office_data)
        bank_accounts_instances = []

        for bank_account_data in bank_accounts_data:
            bank_account_instance = BankAccounts.objects.create(Office=office, **bank_account_data)
            bank_accounts_instances.append(bank_account_instance)


        return {'office': OfficeSerializer(office).data, 'bank_accounts': BankAccountsSerializer(bank_accounts_instances, many=True).data}

