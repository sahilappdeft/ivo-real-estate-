from django.contrib import admin
from .models import Company, Office, BankAccounts, CompanyRole, OfficeUnit, OfficeEmployee

admin.site.register(Company)
admin.site.register(BankAccounts)
admin.site.register(Office)
admin.site.register(CompanyRole)
admin.site.register(OfficeUnit)
admin.site.register(OfficeEmployee)

# Register your models here.
