import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

current_dir = os.path.dirname(os.path.abspath(__file__))

logo_image = os.path.join(current_dir, 'assets', 'images', 'logo.jpg')

def commonEmailInitialize(subject, recipients, text_content=''):
    msg = EmailMultiAlternatives(
        subject=f'Aikona : {subject}',
        body=text_content,
        from_email="nv.test.dev@gmail.com",
        to=recipients
    )
    return msg

def welcome_email(subject, recipients, user_name="N/A"):
    try:
        html_content = render_to_string('welcome_email_template.html', {'user_name': user_name,
                                        })
        text_content = strip_tags(html_content)

        msg = commonEmailInitialize(subject, recipients, text_content)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print('Email sent')
        return True
    except Exception as e:
        print(e)
        return False

def send_verify_email(subject, recipients, otp, user_name="N/A"):
    try:
        html_content = render_to_string('email-templates/email-verification.html', {
                                        'otp': otp, 'user_name': user_name})
        text_content = strip_tags(html_content)

        msg = commonEmailInitialize(subject, recipients, text_content)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print('Email sent')
        return True
    except Exception as e:
        print(e)
        return False


def send_forgot_password_email(subject, recipients, otp, user_name="N/A"):
    try:
        html_content = render_to_string('email-templates/FORGOT.html', {
                                        'otp': otp, 'user_name': user_name})
        text_content = strip_tags(html_content)

        msg = commonEmailInitialize(subject, recipients, text_content)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print('Email sent')
        return True
    except Exception as e:
        print(e)
        return False
    

def send_invite_employee_email(subject, recipient_email, token):
    try:
        html_content = render_to_string('email-templates/invite.html', {'link': token})
        text_content = strip_tags(html_content)

        msg = commonEmailInitialize(subject, [recipient_email], text_content)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print('Email sent')
        return True
    except Exception as e:
        print(e)
        return False
