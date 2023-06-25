from django.urls import path
from userinfo.views import home_page,download_maindb,download_backupdb
urlpatterns = [
    path('',home_page,name="home"),
    path('maindb',download_maindb,page_name="download_bd"),
     path('backupdb',download_backupdbe_name="download_bd"),
]
