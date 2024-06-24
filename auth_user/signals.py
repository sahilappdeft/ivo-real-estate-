from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from office.models import Company
from employee.models import Employee, InviteEmployee
from .utilis import get_user_info

@receiver(post_save, sender=CustomUser)
def create_company(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'company':
            # Create a company instance associated with the user
            # Company.objects.create(user=instance)
            pass
        elif instance.role == 'employee':
            # Create a Employee instance associated with the user
            Employee.objects.create(user=instance)

            # # get user from auth micro-service
            # user = get_user_info(instance.user_id)
            
            # # get invite employee object
            # InviteEmployee.objects.filter()