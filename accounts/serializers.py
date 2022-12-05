from asyncio import log
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User

import re

class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'fname', 'lname']
        extra_kwargs = {'password':{'write_only':True, 'min_length':5,'required':True, 'error_messages':{"required":"password needed"}},
        'email':{'required':True, 'error_messages':{"required":"Email field must not be blank"}},
        'first_name':{'required':True, 'error_messages':{"required":"pass at least first name"}}}

    fname = serializers.CharField()
    lname = serializers.CharField()

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if not re.findall('\d', data['password']):
            raise ValidationError(("The password must contain atleast one digit,0-9"),code='password_no_digit')

        if not re.findall('[a-z]', data['password']):
            raise ValidationError(("The password must contain atleast one lower case alphabet,a-z"),code='password_no_lower')

        if not re.findall('[A-Z]',data['password']):
            raise ValidationError(("The password must contain atleast one uppser case alphabet,A-Z"),code='password_no_upper')

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Username is already taken')

        return data

        

    def create(self, validated_data):
        user  = User.objects.create(fname = validated_data['fname'],
        lname = validated_data['lname'],
        email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError('Account doesnt exist!!')

        return data
    
    def get_jwt_token(self,validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user1 = User.objects.filter(email=email)
        # user1.is_active = True
        user = authenticate(email=email, password=password)   #ye hmesha none dega age is_active false h to

        if not user:
            return {'message':'credentials dont match!', 'data':{}}

        refresh = RefreshToken.for_user(user)

        return {'message':'user logged in successfully!', 'data':{ 'token':{
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }}}