from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# Create your views here.



# def registration_email(user):
#     uid = urlsafe_base64_encode(force_bytes(user))
#     subject = 'Registration'
#     message = 'Thanks for registering with us'
#     sender = 'solomonobonyo74@gmail.com'
#     # sender = settings.
#     send_mail(subject, message, sender, [email], fail_silently=False)



def registration_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    verification_link = f'https://solo-ham.github.io/solonote.github.io/verify-account.html?uid={uid}&token={token}/'
    subject = 'Registration'
    message = f'Thanks for registering with us. Please click the link below to complete your verification:\n{verification_link}'
    sender = 'solomonobonyo74@gmail.com'
    # sender = settings.
    send_mail(subject, message, sender, [user.email], fail_silently=False)