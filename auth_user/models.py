from django.db import models

# Create your models here.

class CustomUser(models.Model):
    ROLE_CHOICES = (
        ('superadmin', 'Superadmin'),
        ('admin', 'Admin'),
        ('company', 'Company'),
        ('employee', 'Employee'),
    )

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    user_id = models.IntegerField(null=False, blank=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES,
                            default="company", null=False, blank=False)

    def __str__(self):
        return str(self.user_id)