from django.shortcuts import render

# Create your views here.

import json
import pdb

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Diary
from . import models


@csrf_exempt
def post_sign_up(request):
    with transaction.atomic():
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email')
        )
        #user.save()
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        userinfo = models.UserInfo(user=user)
        userinfo.save()


    return HttpResponse(
        json.dumps(
            {
                'token': Token.objects.get(user=user).key
            }
        )
    )

@csrf_exempt
def post_experience(request):
    print(request.body)
    #request_dict = json.loads(request.body.decode('utf-8'))

    try:
        token = request.POST.get('token',' ')
        print(token)
    except Exception:
        token = None

    if not token:
        print("No Token found in POST")
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user
    diaries = Diary.objects.all()
    try:

        target_diary = Diary.objects.get(diary_name=request.POST.get('diary_name',''))

    except Exception:
        target_diary = None

    if not target_diary:
        print("No Diary Available")
        return HttpResponse("No diary bro", status=401)

    with transaction.atomic():
        posty = models.Post();
        posty.user = user
        posty.post_text = request.POST.get('post_text', '')
        posty.post_title = request.POST.get('post_title', '')
        posty.diary = target_diary
        posty.post_img = request.POST.get('post_pic_url')
        posty.post_votes = 10
        posty.save()

    return HttpResponse(
        json.dumps(
            {
                'status': 'success'
            }
        )
    )


@csrf_exempt
def get_user_detail(request):
    print request
    token = request.POST.get('token', None)

    print token
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    info = models.UserInfo.objects.filter(user=user)

    if len(info) == 0:
        info = models.UserInfo()
        info.user = user
        info.save()
    else:
        info = info[0]

    return HttpResponse(
        json.dumps(
            {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,

            }
        )
    )


@csrf_exempt
def get_wall_posts(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    followers = models.Follows.objects.filter(user_one=user)

    ret_list_post_username = []

    ret_list_post_title = []

    ret_list_post_text = []

    ret_list_post_pic_url = []

    for follower in followers:
        print follower.user_two

        sub_posts = models.Post.objects.filter(user=follower.user_two)
        print sub_posts

        for j in sub_posts:
            ret_list_post_title.append(j.post_title)
            ret_list_post_text.append(j.post_text)
            ret_list_post_pic_url.append(j.post_img)

            ret_list_post_username.append(j.user.get_username())
        print ret_list_post_title
        print ret_list_post_text

    print ret_list_post_text

    print ret_list_post_title
    print ret_list_post_username

    return HttpResponse(
        json.dumps(
            {
                'post_titles': ret_list_post_title,
                'post_texts': ret_list_post_text,
                'post_usernames': ret_list_post_username,
                'post_pic_url': ret_list_post_pic_url

            }
        )
    )


@csrf_exempt
def get_diary_posts(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    diary_name_respo = request.POST.get('diary_name',None)

    followers = models.Follows.objects.filter(user_one=user)

    target_diary = models.Diary.objects.filter(diary_name=diary_name_respo)

    postyy = models.Post.objects.filter(diary=target_diary.get(diary_name=diary_name_respo))

    ret_list_post_username = []

    ret_list_post_title = []

    ret_list_post_text = []

    ret_list_post_pic_url = []

    for posty in postyy:
        print posty.post_text

        ret_list_post_username.append(posty.user.get_username())

        ret_list_post_title.append(posty.post_title)
        ret_list_post_pic_url.append(posty.post_img)

        ret_list_post_text.append(posty.post_text)

    print ret_list_post_text
    print ret_list_post_username
    print ret_list_post_title
    print ret_list_post_pic_url

    return HttpResponse(
        json.dumps(
            {
                'post_titles': ret_list_post_title,
                'post_texts': ret_list_post_text,
                'post_usernames' : ret_list_post_username,
                'post_pic_url': ret_list_post_pic_url

            }
        )
    )


@csrf_exempt
def post_diary(request):
    print(request.body)
    #request_dict = json.loads(request.body.decode('utf-8'))

    try:
        token = request.POST.get('token',' ')
        print(token)
    except Exception:
        token = None

    if not token:
        print("No Token found in POST")
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user
    diaries = Diary.objects.all()

    with transaction.atomic():
        diary = models.Diary()
        diary.diary_name = request.POST.get('diary_name', '')
        diary.diary_string = request.POST.get('diary_string', '')
        diary.diary_brief = request.POST.get('diary_brief', '')

        diary.save()

    return HttpResponse(
        json.dumps(
            {
                'status': 'success'
            }
        )
    )


def get_diary_postss(request):
    token = request.GET.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    followers = models.Follows.objects.values('user_two_id').filter(user_one=user)

    posty = models.Post.objects.filter(user=user)

    ret_list = []

    for follower in followers:

        curr_dict = {
            'follower_name': follower.user_two.name,

        }

        sub_posts = models.Post.objects.filter(user=follower.user_two)

        post_list = []
        for post_item in sub_posts:
            post_list.append(
                {
                    'post_name': post_item.post_title,
                    'post_title':post_item.post_text,
                    'post_votes':post_item.post_votes,
                    'post_diary':post_item.diary.diary_name,


                }
            )

        curr_dict['posts'] = post_list

        ret_list.append(curr_dict)

    return HttpResponse(
        json.dumps(
            {
                'wall': ret_list
            }
        )
    )


def get_followers(request):
    token = request.GET.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    followers = models.Follows.objects.values('user_two').filter(user_one=user)

    posty = models.Post.objects.filter(user=user)

    ret_list = []
    ret_list_ids = []

    for follower in followers:
        ret_list.append(follower.user_two.name)
        ret_list_ids.append(User.objects.get(user=follower.user_two).id)

    return HttpResponse(
        json.dumps(
            {
                'followers': ret_list,
                'follower_id': ret_list_ids
            }
        )
    )

@csrf_exempt
def follow(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    followee_name = request.POST.get('followee_name', None)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    follow_user = User.objects.get(username=followee_name)

    with transaction.atomic():
        followy = models.Follows()
        followy.user_one = user
        followy.user_two = follow_user
        followy.save()

    return HttpResponse(
        json.dumps(
            {
                'status': 'success'
            }
        )
    )

@csrf_exempt
def get_profile(request):
    token = request.GET.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    name = request.GET.get('name', None)

    target_user = User.objects.get(username=name)

    return HttpResponse(
        json.dumps(
            {
                'first_name': target_user.first_name,
                'last_name': target_user.last_name,
                'username': target_user.username,


            }
        )
    )


#upvote downvote

@csrf_exempt
def get_alldiaries(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user
    list_of_diaries = Diary.objects.all()

    followers = models.Follows.objects.values('user_two').filter(user_one=user)

    posty = models.Post.objects.filter(user=user)

    ret_list = []
    ret_list_ids = []

    for diaries in list_of_diaries:
        ret_list.append(diaries.diary_name)

    print ret_list[0]

    return HttpResponse(
        json.dumps(
            {
                'diaries': ret_list,

            }
        )
    )


@csrf_exempt
def get_user_profile(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user
    name = request.POST.get('name', None)

    name_user = User.objects.filter(username=name)

    print name_user.get(username=name).first_name
    return HttpResponse(
        json.dumps(
            {
                'username': name_user.get(username=name).username,
                'first_name': name_user.get(username=name).first_name,
                'last_name': name_user.get(username=name).last_name,
                'email':name_user.get(username=name).email,


            }
        )
    )


def upvote(request):
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse("Unauthorized", status=401)

    token = Token.objects.filter(key=token)

    if len(token) == 0:
        return HttpResponse("Unauthorized", status=401)

    user = token[0].user

    post_namey = request.POST.get('post_name', None)

    target_post = models.Post.objects.get(post_name=post_namey)

    traget_post_votes = target_post.post_votes

    with transaction.atomic():
        posty = models.Post()
        posty.post_votes = traget_post_votes + 1

        posty.save()

    return HttpResponse(
        json.dumps(
            {
                'status': 'success',


            }
        )
    )