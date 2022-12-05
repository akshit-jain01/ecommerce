from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer

from .models import OTP, User
from .email import send_otp_email

import random
import time

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                'data':serializer.errors,
                'message':'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            send_otp_email(serializer.data['email'])

            return Response({
                'data':serializer.data,
                'message':'congrats your account has been created, please check for otp in your mailbox and activate your account'
            }, status=status.HTTP_201_CREATED)

        except:
            return Response({
                'data':{},
                'message':'something went wrongly'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)


class SignUpOTPVerification(APIView):
    def post(self, request):

        request_otp   = request.data.get("otp",)
        request_email = request.data.get("email")
        if request_email:
            try:
                otp_instance = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                raise ValidationError('Please enter a valid email')
            
            otp = otp_instance.otp
            email = otp_instance.otp_email

            request_time = OTP.objects.get(otp_email__iexact = request_email).time_created
            current_time = int(time.time())

            if current_time - request_time > 300:
                return Response({"status" : "Sorry, entered OTP has expired."}, status = status.HTTP_403_FORBIDDEN)
            
            if str(request_otp) == str(otp) and request_email == email:
                OTP.objects.filter(otp_email__iexact = request_email).delete()
                user.is_active = True
                user.save()

                return Response({
                    'status':'OTP verified, proceed to login.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status':'OTP incorrect.'
                }, status=status.HTTP_400_BAD_REQUEST)
