from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey('auth_user.Customuser', on_delete=models.CASCADE, 
                            null=False, blank=False, related_name="employee")


class EmployeeOffice(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    office = models.ForeignKey('office.Office', on_delete=models.CASCADE)
    role = models.ForeignKey('EmployeeRole', on_delete=models.CASCADE,
                              related_name='employee_role')

    class Meta:
        unique_together = ('employee', 'office', 'role')

    
class EmployeeRole(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    Company = models.ForeignKey('office.Company', on_delete=models.CASCADE, null=False,
                                blank=False, related_name='company_role')


class InviteEmployee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey("office.Office", on_delete=models.CASCADE,
                                related_name='sent_invitations')
    recipient_email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey('EmployeeRole', on_delete=models.CASCADE,
                              related_name='invite_role')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')


class RolePermissiom(models.Model):
    office = models.ForeignKey("office.Office", on_delete=models.CASCADE, 
                               related_name='office_role_permissions')
    role = models.ForeignKey('EmployeeRole', on_delete=models.CASCADE, 
                             related_name='role_permission')
    permission = models.ManyToManyField(Permission)
    
    class Meta:
        unique_together = ('office', 'role')