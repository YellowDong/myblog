from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

# Create your models here.


class Comment(models.Model):
    body = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=225)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.body[:20]
