from django.db import models
from utility.models import  BaseModel
# Create your models here.

class Landlord(BaseModel):
    landlord_id = models.CharField(max_length=50)
    landlord_name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    city_division = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.landlord_name


class LandlordBankAccounts(BaseModel):
    landord = models.ForeignKey('Landlord', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='landlord_banks')
    purpose = models.CharField(max_length=255, null=False, blank=False)
    owner_name = models.CharField(max_length=255, null=False, blank=False)
    iban =  models.CharField(max_length=50, null=False, blank=False)
    bic = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.landlord.landlord_name
    
    
class LandlordContacts(BaseModel):
    pass