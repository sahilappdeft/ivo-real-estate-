from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InviteEmployee
from .utilis import generate_token
from utility.emailTemplates import send_invite_employee_email


@receiver(post_save, sender=InviteEmployee)
def Update_invite_employe_object(sender, instance, created, **kwargs):
    if created:
        token = generate_token(instance.id)
        instance.token = token
        instance.save()
        
        #send invitation mail to employee
        subject = "Invite Employee"
        # generate_link = 
        send_invite_employee_email(subject, [instance.recipient_email], token)
        
