import hashlib

from django.contrib.auth.models import User, Group

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','email','groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    emailmd5 = serializers.SerializerMethodField()

    def get_emailmd5(self, obj):
        return hashlib.md5(str(obj.email).encode('utf-8')).hexdigest()
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','groups', 'emailmd5')
        read_only_fields = ('email',)
