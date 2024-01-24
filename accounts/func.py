from django.conf import settings
from django.core.mail import send_mail
import random

def sendEmailVerification(request, email):
    subject = 'Email Verification'
    otp = random.randint(100000,999999)
    message = f'OTP for verify email is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    return otp