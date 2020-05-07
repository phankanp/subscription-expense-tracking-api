from celery import shared_task
from django.core.management import call_command


@shared_task
def send_email_reminder():
    call_command("email_reminder",)
    return True
