from django.urls import path
from userinfo.views import home_page,download_maindb,download_backupdb
urlpatterns = [
     path('',home_page,name="home"),
     path('maindb',download_maindb,name="download_md"),
     path('backupdb',download_backupdb,name="download_bd"),
]
