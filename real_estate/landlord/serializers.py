from django.db import transaction

from rest_framework import serializers
from .models import (Landlord, LandlordBankAccounts, LandlordContacts)

class Landlordserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Landlord
        fields = '__all__'
        
        
class LandlordBankAccountsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LandlordBankAccounts
        exclude  = ['landord']        

class LandlordContactsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LandlordContacts
        exclude  = ['landord']        


class LandlordContactsAccountsSerializer(serializers.ModelSerializer):
    # building_unit = BuildingUnitSerializer()
    bank_accounts = LandlordBankAccountsSerializer(many=True)
    contacts = LandlordContactsSerializer(many=True)
    
    class Meta:
        model = Landlord
        fields = '__all__'
    
    def create(self, validated_data):
        bank_accounts_data = validated_data.pop('bank_accounts', [])
        contacts_data = validated_data.pop('contacts', [])
        
        try:
            with transaction.atomic():
                    
                # create Landlord object
                landlord = Landlord.objects.create(**validated_data)
                # Create landlord bank accounts for the building unit
                for bank_account_data in bank_accounts_data:
                    account_instance = LandlordBankAccounts.objects.create(landord=landlord,  **bank_account_data)

                # Create contacts of the Landlord
                for contact_data in contacts_data:
                    contact_instance = LandlordContacts.objects.create(landord=landlord, **contact_data)
                
        except Exception as e:
            print(e)
            
            raise serializers.ValidationError({"error":"Failed to create Landlord"})

        return landlord

    def update(self, instance, validated_data):
        bank_accounts_data = validated_data.pop('bank_accounts', [])
        contacts_data = validated_data.pop('contacts', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return Landlordserializer(instance).data