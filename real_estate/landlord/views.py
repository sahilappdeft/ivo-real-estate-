from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from utility.helpers import success, error
from office.models import Company
from auth_user.permission import IsTokenValid
from .models import Landlord, LandlordBankAccounts
from real_estate.property.models import Property
from .serializers import*

# Create your views here.
class LandlordViewset(viewsets.ModelViewSet):
    '''
    This class provide the crud of the Landlord.
    '''
    serializer_class = Landlordserializer
    permission_classes = (IsTokenValid,)
    queryset = Landlord.objects.all()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        property_id = data.pop('property', None)
        # Check if property_id is provided
        if property_id:
            try:
                property = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return Response(error("Property not found", {}), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(error("Property ID is required", {}), status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LandlordContactsAccountsSerializer(data=data)
        if serializer.is_valid():
            landlord_instance = serializer.save()
            # Assign landlord to the property instance 
            property.landlord = landlord_instance
            property.save()
             # Serialize the Landlord instance
            landlord_data = Landlordserializer(landlord_instance).data
            return Response(success("success", landlord_data), status=status.HTTP_201_CREATED)
        return Response(error(serializer.errors, {}), status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        data = request.data.copy()
        serializer = LandlordContactsAccountsSerializer(instance, data=request.data)
        bank_accounts_data = data.pop('bank_accounts', [])
        contacts_data = data.pop('contacts', [])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.save()

                    # Update or create bank accounts detais for the landlord
                    for bank_account_data in bank_accounts_data:
                        account_id = bank_account_data.pop('id', None)
                        is_delete = bank_account_data.pop('is_delete', False)
                        if account_id and not is_delete:
                            room_instance, created = LandlordBankAccounts.objects.update_or_create(
                                id=account_id,
                                defaults={**bank_account_data, 'landlord': instance}
                            )
                        elif is_delete:
                            LandlordBankAccounts.objects.get(id=account_id).soft_delete()
                        else:
                            LandlordBankAccounts.objects.create(landlord=instance, **bank_account_data)

                    # Update or create contact for the landlord
                    for contact_data in contacts_data:
                        contact_id = contact_data.pop('id', None)
                        is_delete = contact_data.pop('is_delete', False)
                        if contact_id and not is_delete:
                            energy_meter_instance, created = LandlordContacts.objects.update_or_create(
                                id=contact_id,
                                defaults={**contact_data, 'landlord': instance}
                            )
                        elif is_delete:
                            LandlordContacts.objects.get(id=contact_id,).soft_delete()
                        else:
                            LandlordContacts.objects.create(landlord=instance, **contact_data)
                            
                    return Response(success("success", data), status=status.HTTP_201_CREATED)
            except LandlordBankAccounts.DoesNotExist:
                return Response(error("Bank account id not found", {}), status=status.HTTP_400_BAD_REQUEST)
            except LandlordContacts.DoesNotExist:
                return Response(error("contact id not found", {}), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(error("something went wrong", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(error(serializer.errors, {}), status=status.HTTP_400_BAD_REQUEST)