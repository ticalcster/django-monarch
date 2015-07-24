from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField()


class Comment(models.Model):
    text = models.CharField(max_length=1000)