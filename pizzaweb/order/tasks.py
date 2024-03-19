from celery import shared_task
from django.core.mail import send_mail

from pizzaweb.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL


@shared_task
def send_email(subject,from_email,message):

    try: send_mail(f'{subject} от {from_email}', message,
                         DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
    except ConnectionRefusedError:
        return 'error'
