# utils.py

from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(email, username):
    send_mail(
        subject="Welcome!",
        message=f"Hello {username}, welcome to our platform.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )