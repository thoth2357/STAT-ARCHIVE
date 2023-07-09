from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import User


def generate_token(user):
    token_generator = PasswordResetTokenGenerator()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    return uid, token

def generate_link(request, uid, token):
    current_site = get_current_site(request)
    verification_url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    verification_link = f'http://{current_site.domain}{verification_url}'
    return verification_link

def decode_token(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        token_generator = PasswordResetTokenGenerator()
        return user, token_generator
    except User.DoesNotExist:
        return None, None
    
def generate_password_reset_token(request, user):
    token = default_token_generator.make_token(user)
    expiration = timezone.now() + timedelta(minutes=10)
    link = request.build_absolute_uri(reverse('reset_password')) + f'?token={token}'
    return token,expiration,link