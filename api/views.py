from django.http import HttpResponse
from rest_framework.response import Response
from api.serializer import register_serializer, user_data,update_data,ChangePasswordSerializer,news_serializer
from userinfo.models import  userdata,phone_verification,email_verification,usernews
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.utils.timezone import utc
import string 
import random
from cryptography.fernet import Fernet
from django.contrib.auth.models import User
import random
import datetime
import requests
from django.core.mail import send_mail
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
def generate_fernetkey(password):
        salt = password.encode()
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend())
        return base64.urlsafe_b64encode(kdf.derive(salt))
class home(APIView):
    def get(self,request):
       return Response({"version":"1.2.4"})
class update_version(APIView):
    def get(self,request):
        with open("Busyness-update",'rb') as f:
            data=f.read()
            response=HttpResponse(data,content_type='application/Busyness-update')
            response["Content-Disposition"]='Attachment; filename="Busyness-update"'
            return response
class news(APIView):
    def get(self,request):
        return Response(news_serializer(usernews.objects.all(),many=True).data)
class get_userinfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.userdata.activated:
            return Response([{"Access":True},register_serializer(request.user).data,user_data(userdata.objects.get(user=request.user)).data])
        else:
            if request.user.userdata.demo:
                delta=datetime.datetime.utcnow().replace(tzinfo=utc)-request.user.date_joined
                if delta.days>31:
                    request.user.userdata.demo=False
                    request.user.userdata.save()
                    return Response([{"Access":False}])
                return Response([{"Access":True,"Demo": 30-delta.days},register_serializer(request.user).data,user_data(userdata.objects.get(user=request.user)).data])
            return Response([{"Access":False}])
    def post(self,request):
        ser=update_data(instance=userdata.objects.get(user=request.user),data=request.data)
        cer=register_serializer(instance=request.user,data=request.data)
        c=False
        if ser.is_valid():
            ser.save()
            c=True
        if cer.is_valid():
            cer.save()
            c=True
        if c:
            return Response({"updated":True})
        else:
            print(ser.errors)
        return Response({"updated":False,"errors":ser.errors})
class register_user(APIView):
    def post(self,request):
        t=register_serializer(data=request.data)
        if t.is_valid():
            c=t.save()
            token_obj,_=Token.objects.get_or_create(user=c)
            y=Fernet(generate_fernetkey(request.data["password"]))
            result_str = ''.join(random.choice(string.ascii_lowercase) for i in range(7))
            userdata.objects.create(user=c,db_password=y.encrypt(result_str.encode()).decode())
            return Response({"token":str(token_obj),"data":t.data,"error":False})
        return Response({"status":403,'error':t.errors})
class phoneverification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.userdata.otp_limit>0:
            try:
                userdata.objects.get(phone_number=request.data["phone_number"])
                return Response({"Already":True})
            except userdata.DoesNotExist:
                pass
                
            try:
                try:
                    c=phone_verification.objects.get(phone_number=request.data["phone_number"])
                    now = datetime.datetime.utcnow().replace(tzinfo=utc)
                    timediff = now - c.created
                    minutes = divmod(timediff.total_seconds(), 60) 
                    if minutes[0]>=5:
                        c.delete()
                    else:
                        return Response({"Wait":True})
                except phone_verification.DoesNotExist:
                    pass
                otp=random.randint(1000,10000)
                request.user.userdata.otp_limit-=1
                request.user.userdata.save()
                v=phone_verification.objects.get(user=request.user)
                v.otp=otp
                requests.get('https://2factor.in/API/V1/a9fbe000-34fe-11ed-9c12-0200cd936042/SMS/+91{}/{}/'.format(request.data["phone_number"],otp))
                v.phone_number=request.data["phone_number"]
                v.save()
                return Response({"otp":"sucess"})
            except phone_verification.DoesNotExist:
                c=random.randint(1000,10000)
                request.user.userdata.otp_limit-=1
                request.user.userdata.save()
                phone_verification.objects.create(user=request.user,phone_number=request.data["phone_number"],otp=c)
                requests.get('https://2factor.in/API/V1/a9fbe000-34fe-11ed-9c12-0200cd936042/SMS/+91{}/{}/'.format(request.data["phone_number"],c))
                return Response({"otp":"sucess"})
        else:
            return Response({"Limit":"over"})
    def post(self,request):
        try:
            phone=phone_verification.objects.get(user=request.user)
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - phone.created
            minutes = divmod(timediff.total_seconds(), 60) 
            if minutes[0]>=5:
                phone.delete()
                return Response({"Expired":True})
            if phone.otp==request.data.get("otp"):
                    request.user.userdata.phoneverfied=True
                    request.user.userdata.phone_number=phone.phone_number
                    request.user.userdata.save()
                    request.user.phone_verification.delete()
                    return Response({"verified":True})
            return Response({"verified":False})
        except phone_verification.DoesNotExist:
            return Response({"error":True})
class emailverification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.userdata.otp_limit>0:
            try:
                User.objects.get(email=request.data["email"])
                return Response({"Already":True})
            except Exception as e:
                pass
            try:
                try:
                    c=email_verification.objects.get(email=request.data["email"])
                    now = datetime.datetime.utcnow().replace(tzinfo=utc)
                    timediff = now - c.created
                    minutes = divmod(timediff.total_seconds(), 60) 
                    if minutes[0]>=5:
                        c.delete()
                    else:
                        return Response({"Already":True})
                except email_verification.DoesNotExist:
                        pass
                otp=random.randint(1000,10000)
                v=email_verification.objects.get(user=request.user)
                v.otp=otp
                send_mail('Busyness', 'Dear {},Your Otp is {}'.format(request.user.username,otp), 'devendran635@gmail.com', [request.data["email"]])
                v.email=request.data["email"]
                v.save()
                request.user.userdata.otp_limit-=1
                request.user.userdata.save()
                return Response({"otp":"sucess"})
            except email_verification.DoesNotExist:
                c=random.randint(1000,10000)
                request.user.userdata.otp_limit-=1
                request.user.userdata.save()
                email_verification.objects.create(user=request.user,email=request.data["email"],otp=c)
                send_mail('Busyness', 'Dear {},Your Otp is {}'.format(request.user.username,c), 'devendran635@gmail.com', [request.data["email"]])
                return Response({"otp":"sucess"})
        else:
            return Response({"Limit":"over"})
    def post(self,request):
        try:
            email=email_verification.objects.get(user=request.user)
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - email.created
            minutes = divmod(timediff.total_seconds(), 60) 
            if minutes[0]>=5:
                email.delete()
                return Response({"Expired":True})
            if email.otp==request.data.get("otp"):
                    request.user.userdata.emailverfied=True
                    request.user.email=email.email
                    request.user.userdata.save()
                    request.user.email_verification.delete()
                    return Response({"verified":True})
            return Response({"verified":False})
        except email_verification.DoesNotExist:
            return Response({"error":True})




