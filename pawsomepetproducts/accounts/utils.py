import random
from django.core.mail import send_mail


#functions to be used in views

#functtion for genrating an otp
def generate_otp():
    return random.randint(100000,999999)



#function for sending otp email to user
def send_otp_email(email, otp):
    subject = 'Email Verification OTP'
    message = f'Thanks for registering in Pawsome. Your OTP for email verification is: {otp}'
    from_email = 'bithulmb07@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)