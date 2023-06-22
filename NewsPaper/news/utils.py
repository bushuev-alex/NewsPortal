from datetime import datetime
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext


def too_many_posts(model, post) -> bool:
    posts = model.objects.filter(author=post.author).filter(date_time__gte=datetime.today().date())
    if len(posts) > 20:
        return True
    return False


msg = gettext("You've posted 3 news today already. Today you are not allowed to post any. Wait for tomorrow.")
