from datetime import datetime
from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class UserInfo(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)
    join_date = models.DateTimeField('Join published',default='2011-11-11 11:11')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Diary(models.Model):

    def __str__(self):
        return self.diary_name

    diary_name = models.CharField(max_length=30)
    diary_brief = models.CharField(max_length=300)
    diary_string = models.CharField(max_length=1000,null=True)


class Post(models.Model):

    def __str__(self):
        return self.post_title

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=30)
    post_text = models.CharField(max_length=200)
    post_img = models.CharField(max_length=1000,null=True,blank=True)
    diary = models.ForeignKey(Diary)
    post_votes = models.IntegerField(null=True,blank=True)


class Follows(models.Model):

    def __str__(self):
        return str(self.user_one) +'-' + str(self.user_two)

    user_one = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="who")
    user_two = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="whom")






