from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора
        posts = Post.objects.filter(author=self, type='POST')
        articles_rating = sum((post.rating for post in posts))

        # суммарный рейтинг всех комментариев автора
        comments = Comment.objects.filter(user=self.user)
        comments_by_author_rating = sum((comment.rating for comment in comments))

        # суммарный рейтинг всех комментариев к статьям автора.
        posts = Post.objects.filter(author=self, type='POST')
        sets_of_comments = (Comment.objects.filter(post=post) for post in posts)

        comments_to_author_rating = 0
        for set_ in sets_of_comments:
            for comment in set_:
                comments_to_author_rating += comment.rating

        self.rating = articles_rating * 3 + comments_by_author_rating + comments_to_author_rating
        self.save()

    def __str__(self):
        return f"{self.user}: rating {self.rating}"


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    post = 'POST'
    news = 'NEWS'

    POST_TYPE = [
        (post, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=4,
                            choices=POST_TYPE,
                            default=post)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=30)
    text = models.TextField()
    rating = models.IntegerField(null=False, default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return self.text[:len(self.text)]
        return self.text[:124] + "..."

    def __str__(self):
        return f"{self.title}: {self.text[:124]}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=False, default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
