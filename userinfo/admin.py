from django.contrib import admin
from userinfo.models import userdata,phone_verification,email_verification,usernews,FileModel
admin.site.register(userdata)
admin.site.register(phone_verification)
admin.site.register(email_verification)
admin.site.register(usernews)
admin.site.register(FileModel)
