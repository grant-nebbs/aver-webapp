from django.db import models


# Create your models here.
class User(models.Model):
    userId = models.IntegerField()
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    createdDate = models.DateTimeField()


class Post(models.Model):
    postId = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    createdDate = models.DateTimeField()
    score = models.IntegerField()
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=100)
