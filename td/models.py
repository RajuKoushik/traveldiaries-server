from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    user_id = models.IntegerField()
    nick_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    join_date = models.DateTimeField('Join published')



    def __str__(self):
        return self.nick_name

        # adding a custom database


class TravelDiary(models.Model):
    loc_id = models.IntegerField()
    loc_name = models.CharField(max_length=30)
    loc_text = models.CharField(max_length=200)


    def __str__(self):
        return self.choice_text

class Post(models.Model):
    post_id = models.IntegerField()
    post_title = models.CharField(max_length=30)
    post_text = models.CharField(max_length=200)

    post_votes = models.IntegerField()

    def __str__(self):
        return self.post_title

class TravelConnection(models.Model):
    user_id = models.ForeignKey(User)
    post_id = models.ForeignKey(Post)
    loc_id = models.ForeignKey(TravelDiary)

    def __str__(self):
        return self.user_id

class Follows(models.Model):
    user_id_one = models.ForeignKey(User, related_name="who")
    user_id_two = models.ForeignKey(User, related_name="whom")






