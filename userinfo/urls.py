from django.urls import path
from userinfo.views import home_page,download_maindb,download_backupdb
urlpatterns = [
    path('',home_page,name="home"),
    path('backupdb',home_page,page_name="download_bd"),
     path('backupdb',home_page,page_name="download_bd"),
]
