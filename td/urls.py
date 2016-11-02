from django.conf.urls import url
from rest_framework.authtoken import views as rest_views
from . import views

urlpatterns = [
    url(r'^login/', rest_views.obtain_auth_token),
    url(r'^signup/?', views.post_sign_up),
    url(r'^get/user_details', views.get_user_detail),

]
