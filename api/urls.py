
from django.urls import path
from api.views import get_userinfo, phoneverification,register_user,emailverification,home,news,update_version
from rest_framework.authtoken import views
urlpatterns = [
    path('',home.as_view(),name="api-token"),
    path('getnews/',news.as_view(),name="news"),
    path('login/',views.obtain_auth_token,name="api-token"),
    path('update/',update_version.as_view(),name="update"),
    path("user/",get_userinfo.as_view(),name="info"),
    path("register/",register_user.as_view(),name="register"),
    path("phone/verification/",phoneverification.as_view(),name="phone_verfication"),
     path("email/verification/",emailverification.as_view(),name="email_verfication")
]
