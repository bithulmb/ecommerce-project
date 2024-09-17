import random

from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client

# functions to be used in views


# functtion for genrating an otp
def generate_otp():
    return random.randint(100000, 999999)


# function for sending otp email to user
def send_otp_email(email, otp):
    subject = "Email Verification OTP"
    message = f"Hii There. \n \n Your OTP for email verification is: {otp}\n \n Best regards,\n Pawsome Pet Products"
    from_email = "bithulmb07@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_otp_mobile(mobile_number, otp):
    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

    message = f"Your OTP for Mobile verification is: {otp}"
    mobile = "+91" + str(mobile_number)
    print(mobile)
    client.messages.create(body=message, from_=settings.TWILIO_PHONE_NUMBER, to=mobile)
