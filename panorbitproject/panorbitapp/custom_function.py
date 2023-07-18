from __future__ import print_function
import panorbitproject.settings as stng
import random
from django.core.mail import send_mail


def random_number(start: int, end: int):
    return random.randint(start, end)


def send_email(subject, message_body,receiver_email_id):
    send_mail(subject, message_body,stng.EMAIL_HOST_USER,[receiver_email_id])

