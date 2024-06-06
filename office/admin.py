from django.contrib import admin
from .models import Company, Office, BankAccounts, CompanyRole, RolePermissiom

admin.site.register(Company)
admin.site.register(BankAccounts)
admin.site.register(Office)
admin.site.register(CompanyRole)
admin.site.register(RolePermissiom)

# Register your models here.
