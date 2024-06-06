from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company, CompanyRole

@receiver(post_save, sender=Company)
def create_company(sender, instance, created, **kwargs):
    
    if created:
        default_roles = ['admin', 'social worker', 'backend']
        for role in default_roles:
            CompanyRole.objects.create(name=role, Company=instance)