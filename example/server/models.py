from django.db import models


class Address(models.Model):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)


class Group(models.Model):
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField()


class Comment(models.Model):
    text = models.CharField(max_length=1000)
