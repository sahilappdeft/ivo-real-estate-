from django.db import models
from django.contrib.auth.models import Permission

#Choices for employee role
ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('backend', 'Backend'),
        ('social_worker', 'Social Worker'),
    ]


class Company(models.Model):
    user = models.OneToOneField('auth_user.Customuser', on_delete=models.CASCADE, 
                                null=False, blank=False, related_name='company_user')


class OfficeUnit(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    cost_center = models.CharField(max_length=255)
    head_1 = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL,
                               related_name='unit_head_1', null=True, blank=True)
    head_2 = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL,
                               related_name='unit_head_2', null=True, blank=True)
    head_3 = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL,
                               related_name='unit_head_3', null=True, blank=True)
    offices = models.ManyToManyField('Office', related_name='office_units')
    

class Office(models.Model):
    HEAD_OFFICE = 'headoffice'
    NORMAL_OFFICE = 'normaloffice'

    OFFICE_TYPE_CHOICES = [
        (HEAD_OFFICE, 'Head Office'),
        (NORMAL_OFFICE, 'Normal Office'),
    ]

    name = models.CharField(max_length=265, null=False, blank=False)
    purpose = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    zipcode = models.CharField(max_length=255, null=False, blank=False)
    city_division = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    office_email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    cost_center = models.CharField(max_length=255, null=False, blank=False)
    office_type = models.CharField(max_length=100, choices=OFFICE_TYPE_CHOICES,
                                    default=NORMAL_OFFICE)
    user = models.ForeignKey('auth_user.Customuser', on_delete=models.CASCADE, 
                                null=False, blank=False, related_name="office")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=False,
                                blank=False, related_name="company_office")

    def __str__(self):
        return self.name


class BankAccounts(models.Model):
    Office = models.ForeignKey('Office', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='offic_banks')
    purpose = models.CharField(max_length=255, null=False, blank=False)
    owner_name = models.CharField(max_length=255, null=False, blank=False)
    iban =  models.CharField(max_length=50, null=False, blank=False)
    bic = models.CharField(max_length=50, null=False, blank=False)
    

class RolePermissiom(models.Model):
    company = models.ForeignKey("Company", on_delete=models.CASCADE, 
                               related_name='company_role_permissions', null=True, blank=True)
    role = models.ForeignKey('CompanyRole', on_delete=models.CASCADE, 
                             related_name='role_permission')
    permission = models.ManyToManyField(Permission)
    
    # class Meta:
    #     unique_together = ('company', 'role')
        

class CompanyRole(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    Company = models.ForeignKey('Company', on_delete=models.CASCADE, null=False,
                                blank=False, related_name='company_role')