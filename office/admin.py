from django.contrib import admin
from .models import Company, Office, BankAccounts, CompanyRole, OfficeUnit

admin.site.register(Company)
admin.site.register(BankAccounts)
admin.site.register(Office)
admin.site.register(CompanyRole)
admin.site.register(OfficeUnit)
# Register your models here.
