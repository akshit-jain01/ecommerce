import random, time
from django.core.mail import send_mail
from django.conf import settings

from .models import OTP

def send_otp_email(email):
    
    OTP.objects.filter(otp_email__iexact = email).delete()
    subject = "Your Account verification email"
    otp = random.randint(1000,9999)
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST
    # msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">Swaad</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Looks like you forgot your password. No worries we are here to help you recover your account. Use the following OTP to recover your account and start ordering the delicacies again in no time. <br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Swaad</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>Swaad</p><p>Boys Hostel, Near Girl Hostel AKGEC</p><p>Ghaziabad</p></div></div></div>' , 'swaad.info.contact@gmail.com', (email,))
    # msg.content_subtype = "html"
    # msg.send()
    send_mail(subject, message, email_from, [email])

    time_created = int(time.time())

    otp_obj = OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)
    otp_obj.save()