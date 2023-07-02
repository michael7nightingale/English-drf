from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
import six


class ActivationUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.username)
        )


def get_activation_token(user) -> str:
    return ActivationUserTokenGenerator().make_token(user=user)


def check_activation_token(user, token: str) -> bool:
    return ActivationUserTokenGenerator().check_token(user=user, token=token)


def send_email(request, user, user_email):
    message_subject = "Activate your user account."
    message_content = render_to_string(
        template_name="users/email_activation.html",
        context={
            "user": user.username,
            "protocol": "https" if request.is_secure() else "http",
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": get_activation_token(user)
        }
    )
    message = EmailMessage(subject=message_subject, body=message_content, to=[user_email])
    if message.send():
        return (
            f"{user.username}! Please, check your email {user_email} and follow the link"
            "in the message we have send you to finish the registration."
        )
    else:
        return "Could not send message with the link(((."


def decode_uid(uid: str):
    return force_str(urlsafe_base64_decode(uid))
