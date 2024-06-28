from django.core.mail import send_mail
from django.conf import settings
import random

def otp_generator():
    otp=random.randrange(100000,999999)
    return otp

def mail(email):
    subject="OTP!"
    otp=otp_generator()
    msg=f"""welcome
    
    your otp is \n\n{otp} 
    """
    print(email)
    send_mail(subject, msg, settings.EMAIL_HOST,[email])  
    return otp
