from django.core.mail import send_mail
from django.conf import settings


def Test_email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['flokain11@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
