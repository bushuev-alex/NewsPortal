import time

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from datetime import datetime, timedelta

from news.models import PostCategory, Post, Category


@shared_task
def printer2():
    time.sleep(3)
    print("Hello from signals!")


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string("post_created_email.html",
                                    {
                                        "text": preview,
                                        "link": f"{settings.SITE_URL}/posts/{pk}",
                                    })

    msg = EmailMultiAlternatives(subject=title,
                                 body="",
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscribers)

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def notify_about_new_creation(pk: int, **kwargs):
    post = Post.objects.get(id=pk)
    categories = post.category.all()
    recipient_list = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        recipient_list += [s.email for s in subscribers]

    send_notifications(post.text, post.pk, post.title, recipient_list)
    return True


@shared_task
def notify_about_posts_mon_8am():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_time__gte=last_week)
    categories = set(posts.values_list("category__name", flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list("subscribers__email", flat=True))

    html_content = render_to_string("daily_post.html", {"link": settings.SITE_URL,
                                                        "posts": posts
                                                        }
                                    )
    msg = EmailMultiAlternatives(subject="Posts for a week",
                                 body="",
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscribers)

    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True
