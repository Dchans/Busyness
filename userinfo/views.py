from django.shortcuts import render
from django.http import FileResponse
def home_page(request):
    return render(request,'homepage.html')
def download_maindb(request):
    response =  FileResponse(open("main.db", 'rb'))
    response['Content-Disposition'] = 'attachment; filename="main.db"'
    return response
        
def download_backupdb(request):
    response =  FileResponse(open("backup.db", 'rb'))
    response['Content-Disposition'] = 'attachment; filename="backup.db"'
    return response

   

