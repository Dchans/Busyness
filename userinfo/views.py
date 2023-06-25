from django.shortcuts import render
from django.http import FileResponse
def home_page(request):
    return render(request,'homepage.html')
def download_maindb(request):
     with open("backup.db", 'rb') as file:
         file_name = "main.db"
         response = FileResponse(file, content_type='text/plain')
         response['Content-Disposition'] = 'attachment; filename="main.db"'
         return response
def download_maindb(request):
     with open("backup.db", 'rb') as file:
         file_name = "backup.db"
         response =  FileResponse(file, content_type='text/plain')
         response['Content-Disposition'] = 'attachment; filename="backup.db"'
         return response

   

