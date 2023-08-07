from django.db.models.signals import post_save
from django.dispatch import receiver
from Authentication.models import User
from Authentication.tasks import send_email_func

from .models import Report
from django.contrib.auth.models import Group
from django.db.models import Q


@receiver(post_save, sender=Report)
def send_report_email(sender, instance, created, **kwargs):
    if created:
        #get users in librarian group
        users = User.objects.filter(Q(groups__name=Group.objects.get(name='Librarian')))
        emails = list(users.values_list('email', flat=True))
        
        #send email to all users in librarian group
        for email in emails:
            send_email_func.delay("Librarian", email, 'Sta Archive Resource Report' ,"A user Has reported a resource",type_="report")
