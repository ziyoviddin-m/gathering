from celery import shared_task
from django.core.mail import send_mail




@shared_task
def send_collect_email(user_email, title):
    send_mail(
        "Создание сбора",
        f"Вы только что создали сбор для '{title}'",
        "univerziyo@gmail.com",
        [user_email],
        fail_silently=True
    )

@shared_task
def send_payment_email(user_email, collect, payment_amount):
    send_mail(
        "Подтверждение пожертвования!",
        f"Вы только что сделали пожертвование в размере {payment_amount} руб., к сбору '{collect}'",
        "univerziyo@gmail.com",
        [user_email],
        fail_silently=True
    )