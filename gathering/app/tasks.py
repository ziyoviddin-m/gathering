from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject, message, user_email):
    send_mail(
        subject,
        message,
        "univerziyo@gmail.com",
        [user_email],
        fail_silently=True
    )

@shared_task
def send_collect_email(user_email, title):
    subject = "Создание сбора"
    message = f"Вы только что создали сбор для '{title}'"
    send_email.delay(subject, message, user_email)

@shared_task
def send_payment_email(user_email, collect, payment_amount):
    subject = "Подтверждение пожертвования!"
    message = f"Вы только что сделали пожертвование в размере {payment_amount} руб., к сбору '{collect}'"
    send_email.delay(subject, message, user_email)
