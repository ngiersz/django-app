from django.core.mail import send_mail
from django.conf import settings


def send_email_about_changed_status(order):
    receiver = order.client.email
    subject, message = get_subject_and_message(order)
    send_email(receiver, subject, message)


def get_subject_and_message(order):
    return (f"Status of your order \"{order.title}\"  changed",
            (f"Status of your order\n"
             f"\t\"{order.title}\"\n"
             f"\tCreated date: {order.created_date}\n"
             f"\tFrom: {order.pickupAddress}\n"
             f"\tTo: {order.deliverer}\n"
             f"changed to: {order.status}.\n"
             f"Your deliverer's username is {order.deliverer}")
            )


def send_email(receiver, subject, message):
    send_mail(subject=subject,
              message=message,
              recipient_list=[receiver],
              from_email=settings.EMAIL_HOST_USER)
