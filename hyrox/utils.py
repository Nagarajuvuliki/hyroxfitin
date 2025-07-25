# # accounts/utils.py
# import random
# import string
# from django.core.mail import send_mail
# from django.conf import settings
# from twilio.rest import Client
# from django.utils import timezone
# from datetime import timedelta

# def generate_otp(length=6):
#     """Generate a 6-digit OTP."""
#     characters = string.digits
#     return ''.join(random.choice(characters) for _ in range(length))

# class MessageHandler:
#     def __init__(self, phone_number=None, email=None, otp=None):
#         self.phone_number = phone_number
#         self.email = email
#         self.otp = otp

#     def send_otp_via_sms(self):
#         """Send OTP via Twilio SMS."""
#         if not self.phone_number:
#             return False
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         try:
#             message = client.messages.create(
#                 body=f'Your OTP for MyWebsite is: {self.otp}',
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=f'{settings.COUNTRY_CODE}{self.phone_number}'
#             )
#             return True
#         except Exception as e:
#             print(f"Twilio error: {e}")
#             return False

#     def send_otp_via_email(self):
#         """Send OTP via email."""
#         if not self.email:
#             return False
#         try:
#             send_mail(
#                 subject='Your OTP for MyWebsite Registration',
#                 message=f'Your OTP is {self.otp}. It expires in 5 minutes.',
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[self.email],
#                 fail_silently=False,
#             )
#             return True
#         except Exception as e:
#             print(f"Email error: {e}")
#             return False