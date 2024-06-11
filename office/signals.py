from django.db.models.signals import post_save
from django.dispatch import receiver
from .utilis import create_company_role_and_permissions

from .models import Company, CompanyRole

@receiver(post_save, sender=Company)
def create_company(sender, instance, created, **kwargs):
    
    if created:
        # create default roles and permissions
        create_company_role_and_permissions(instance)