from django.db import models
from django.contrib.auth.models import User
class userdata(models.Model):
    user=models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="default_img_br3s1z.png", null=True, blank=True)
    shopname=models.CharField(max_length=50,default="Nill", null=False, blank=False)
    phone_number=models.CharField(max_length=15,default="Nill", null=False, blank=False)
    address=models.CharField(max_length=200,default="Nill", null=False, blank=False)
    licenseno=models.CharField(max_length=10,default="Nill", null=False, blank=False)
    db_password=models.CharField(max_length=200,default="Nill", null=False, blank=False)
    demo=models.BooleanField(default=True)
    activated=models.BooleanField(default=False)
    phoneverfied=models.BooleanField(default=False)
    emailverfied=models.BooleanField(default=False)
    otp_limit=models.IntegerField(default=6)
    def __str__(self):
        return self.user.username
class phone_verification(models.Model):
    user=models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15,default="Nill", null=False, blank=False)
    otp=models.CharField(max_length=5,default="0", null=False, blank=False)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class email_verification(models.Model):
    user=models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    email=models.EmailField(max_length=254)
    otp=models.CharField(max_length=5,default="0", null=False, blank=False)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class usernews(models.Model):
    image=models.ImageField(null=True,blank=True)
    news_type=models.IntegerField()
    def __str__(self):
        return self.image.name
    
