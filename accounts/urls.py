from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('register/verify', SignUpOTPVerification.as_view()),
    path('login/', LoginView.as_view()),
]
