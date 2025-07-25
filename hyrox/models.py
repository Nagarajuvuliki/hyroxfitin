# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# class UserProfile(models.Model):
#     user =  models.CharField(max_length=50, blank=True, null=True)
#     first_name = models.CharField(max_length=50, blank=True, null=True)
#     last_name = models.CharField(max_length=50, blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional for SMS OTP

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.user.username})"

class OTP(models.Model):
    user =  models.CharField(max_length=50, blank=True, null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP {self.otp} for {self.user.username}"

