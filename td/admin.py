from django.contrib import admin
from .models import UserInfo,Diary, Post , Follows


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Diary)
admin.site.register(Post)

admin.site.register(Follows)
