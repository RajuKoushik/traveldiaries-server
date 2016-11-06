from django.conf.urls import url
from rest_framework.authtoken import views as rest_views
from . import views

urlpatterns = [

    url(r'^login/', rest_views.obtain_auth_token),
    url(r'^signup/?', views.post_sign_up),
    url(r'^get/user_details', views.get_user_detail),
    url(r'^post/post', views.post_post),
    url(r'^post/post_diary', views.post_diary),
    url(r'^get/followers', views.get_followers),
    url(r'^get/diary_posts', views.get_diary_posts),
    url(r'^get/wall_posts', views.get_wall_posts),
    url(r'^follow', views.follow),

]
