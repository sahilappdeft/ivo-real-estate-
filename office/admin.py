from django.contrib import admin
from .models import Company, Office, BankAccounts, CompanyRole

admin.site.register(Company)
admin.site.register(BankAccounts)
admin.site.register(Office)
admin.site.register(CompanyRole)

# Register your models here.
