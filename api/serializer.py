
from rest_framework import serializers
from userinfo.models import *
class user_data(serializers.ModelSerializer):
    email=serializers.ReadOnlyField(source='user.email')
    class Meta:
        model=userdata
        fields="__all__"
class news_serializer(serializers.ModelSerializer):
    class Meta:
        model=usernews
        fields="__all__"
class update_data(serializers.ModelSerializer):
    class Meta:
        model=userdata
        fields=("address","phone_number","shopname","profile_pic","licenseno")
class register_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password"]
        extra_kwargs={'password':{'write_only':True}}
    def create(self,data):
        user=User.objects.create(username=data["username"])
        user.set_password(data["password"])
        user.save()
        return user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
