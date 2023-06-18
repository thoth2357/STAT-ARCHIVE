# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from celery.exceptions import MaxRetriesExceededError
from time import sleep

@shared_task(bind=True, max_retries=3)
def send_verification_email(self, email,subject,message):
    try:
        # Code to send the verification email
        # Use Django's send_mail() function or any email sending library of your choice
        send_mail(
            subject, 
            message, 
            'noreply@example.com', 
            [email])

    except Exception as e:
        # Retry the task in case of failure
        delay = 2 ** self.request.retries  # exponential backoff delay
        if self.request.retries == self.max_retries:
            # Maximum number of retries exceeded
            # Log the error or handle it as required
            print(f"Email sending failed for {email}. Max retries exceeded.")
        else:
            # Retry the task after the delay
            print(f"Email sending failed for {email}. Retrying in {delay} seconds.")
            sleep(delay)
            self.retry(exc=e)
