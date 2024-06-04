from django.contrib import admin
from .models import Company, Office, BankAccounts

admin.site.register(Company)
admin.site.register(BankAccounts)
admin.site.register(Office)
# Register your models here.
