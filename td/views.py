from django.shortcuts import render

# Create your views here.

import json

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from . import models

@csrf_exempt
def post_sign_up(request):
    with transaction.atomic():
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email')
        )
        user.save()
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        userinfo = models.UserInfo(user=user)
        userinfo.save()

    return HttpResponse(
        json.dumps(
            {
                'token': Token.objects.get(user=user).key
            }
        )
    )

