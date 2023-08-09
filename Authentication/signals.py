from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User
from .tasks import send_email_func

@receiver(pre_save, sender=User)
def user_is_approved(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        pass  # New user instance, no need to check approval change
    else:
        if user.is_approved != instance.is_approved:
            if instance.is_approved:
                email = instance.email
                send_email_func.delay(f"{instance.fullname}", email, 'Your account has been approved' ,"",type_="notify_approve",username=email)
