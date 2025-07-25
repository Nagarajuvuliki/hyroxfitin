from django.contrib import admin

# Register your models here.
from hyrox.models import UserProfile,OTP
admin.site.register(UserProfile)
admin.site.register(OTP)