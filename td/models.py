from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
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

    loc_name = models.CharField(max_length=30)
    loc_string = models.CharField(max_length=200)


    def __str__(self):
        return self.loc_name

class Post(models.Model):

    post_title = models.CharField(max_length=30)
    post_text = models.CharField(max_length=200)
    user_id = models.ForeignKey(User)
    loc_id = models.ForeignKey(TravelDiary)
    post_votes = models.IntegerField()

    def __str__(self):
        return self.post_title




class Follows(models.Model):
    user_id_one = models.ForeignKey(User, related_name="who")
    user_id_two = models.ForeignKey(User, related_name="whom")






