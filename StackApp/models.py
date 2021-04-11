from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    asked_question = models.BooleanField()
    multiple_questions = models.BooleanField()


class Post(models.Model):
    postId = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    score = models.IntegerField()
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=100)
