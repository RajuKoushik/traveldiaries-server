from django.contrib import admin
from .models import User,TravelDiary, Post , TravelConnection , Follows


# Register your models here.
admin.site.register(User)
admin.site.register(TravelDiary)
admin.site.register(Post)
admin.site.register(TravelConnection)
admin.site.register(Follows)
