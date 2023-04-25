from celery import shared_task
import time
from .signals import send_notifications


@shared_task
def printer():
    time.sleep(5)
    print("Hello!")


# @shared_task
# # @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_creation(sender, instance, **kwargs):
#     if kwargs["action"] == "post_add":
#         categories = instance.category.all()
#         recipient_list = []
#
#         for cat in categories:
#             subscribers = cat.subscribers.all()
#             recipient_list += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, recipient_list)
