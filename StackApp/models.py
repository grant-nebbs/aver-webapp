from django.db import models


# Create your models here.
class User(models.Model):
    id = models.IntegerField()
    name = models.CharField()
    link = models.CharField()
    createdDate = models.DateTimeField()


class Post(models.Model):
    id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE())
    owner = models.ForeignKey(User, on_delete=models.CASCADE())
    createdDate = models.DateTimeField()
    score = models.IntegerField()
    type = models.CharField()
    title = models.CharField()
    contents = models.CharField()
