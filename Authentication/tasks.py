# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from time import sleep
from .utils import get_librarian_for_level
from Log.models import Log
from typing import Optional


@shared_task(bind=True, max_retries=3)
def send_email_func(self, user, email:Optional[str], subject, message, type_, username:Optional[str]=None):
    try:
        context = {
            'username': user,
            'verification_link': message
        }
        # Code to send the verification email
        # Use Django's send_mail() function or any email sending library of your choice
        if type_ == "verify":
            html_message = render_to_string('Auth/verify_email.html', context)
        elif type_ == "report":
            html_message = render_to_string('Auth/report_resource_email.html', context)
        elif type_ == "approve":
            email = get_librarian_for_level(username)
            html_message = render_to_string('Auth/approve_user_notice_librarian.html', context)
        elif type_ == "notify_approve":
            html_message = render_to_string('Auth/approve_user_notice_user.html',context)
        else:
            html_message = render_to_string('Auth/forgot_password_email.html', context)
        # print(html_message, "message-html")
        send_mail(subject, message="", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email], html_message=html_message)

    except Exception as error_message:
        # Retry the task in case of failure
        delay = 2**self.request.retries  # exponential backoff delay
        if self.request.retries == self.max_retries:
            # Maximum number of retries exceeded
            # Log the error
            Log.objects.create( 
                GeneratedBy="send email",
                ExceptionMessage=f"Email sending failed for {email}. Max retries exceeded.\n{error_message}",
            )
        else:
            # Retry the task after the delay
            Log.objects.create(
                GeneratedBy="send email",
                ExceptionMessage=f"Email sending failed for {email}.\n{error_message}",
            )
            print(f"Email sending failed for {email}. Retrying in {delay} seconds.")
            sleep(delay)
            self.retry(exc=error_message)
