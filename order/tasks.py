from celery import shared_task
from OnlineShop import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


@shared_task()
def order_email_sender(order_id, user_email):
    subject = 'The order was placed'
    message = f'Your order {order_id} has been registered and is being tracked\nhis message has been sent to you by Abbas Moradi online shop'
    email_from = settings.EMAIL_HOST_USER
    try:
        send_mail(subject,message,email_from,[user_email],fail_silently=False,)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")