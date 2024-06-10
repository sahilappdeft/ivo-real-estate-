from django.db import models
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save


class BulkCreateManager(models.Manager):
    def bulk_creatBulkCreateManagere(self, objs, **kwargs):
        created_objs = super().bulk_create(objs, **kwargs)
        for obj in created_objs:
            post_save.send(sender=obj.__class__, instance=obj, created=True)
        return created_objs


# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey('auth_user.Customuser', on_delete=models.CASCADE, 
                            null=False, blank=False, related_name="employee")
    role = models.ForeignKey('office.CompanyRole', on_delete=models.CASCADE,
                              related_name='employee_role', null=True, blank=True)
    office = models.ManyToManyField('office.Office', related_name='employee_offices',
                                    null=True, blank=True)

class InviteEmployee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey("office.Office", on_delete=models.CASCADE,
                                related_name='sent_invitations')
    recipient_email = models.EmailField()
    token = models.CharField(max_length=100)
    role = models.ForeignKey('office.CompanyRole', on_delete=models.CASCADE,
                              related_name='invite_role')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    objects = BulkCreateManager()



