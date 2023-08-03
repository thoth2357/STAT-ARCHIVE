# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from time import sleep
from Log.models import Log


@shared_task(bind=True, max_retries=3)
def send_email(self, email, subject, message):
    try:
        context = {
            
            'username': email.split('@')[0],
            'verification_link': message
        }
        # Code to send the verification email
        # Use Django's send_mail() function or any email sending library of your choice
        
        html_message = render_to_string('Auth/verify_email.html', context)
        # print(html_message, "message-html")
        send_mail(subject, message="", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email], html_message=html_message)

    except Exception:
        # Retry the task in case of failure
        delay = 2**self.request.retries  # exponential backoff delay
        if self.request.retries == self.max_retries:
            # Maximum number of retries exceeded
            # Log the error or handle it as required
            Log.objects.create(
                GeneratedBy="send email",
                ExceptionMessage=f"Email sending failed for {email}. Max retries exceeded.\n{Exception}",
            )
        else:
            # Retry the task after the delay
            Log.objects.create(
                GeneratedBy="send email",
                ExceptionMessage=f"Email sending failed for {email}. Max retries exceeded.\n{Exception}",
            )
            print(f"Email sending failed for {email}. Retrying in {delay} seconds.")
            sleep(delay)
            self.retry(exc=Exception)
