from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InviteEmployee
from .utilis import generate_token, generate_token_link
from utility.emailTemplates import send_invite_employee_email
from auth_user.utilis import get_user_info

@receiver(post_save, sender=InviteEmployee)
def Update_invite_employe_object(sender, instance, created, **kwargs):
    if created:
        token = generate_token(instance.id)
        instance.token = token
        instance.save()
        
        #send invitation mail to employee
        subject = "Invite Employee"
        
        # check user with this email already in company then send another email that say you have added to this office
        
        # generate invite link 
        invite_link = generate_token_link(token)
        send_invite_employee_email(subject, instance.recipient_email, invite_link)
        
