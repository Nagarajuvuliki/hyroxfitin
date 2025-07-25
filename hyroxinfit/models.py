from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from multiselectfield import MultiSelectField
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]

    WORKOUT_CHOICES = [
        ('running', 'Running'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('hiit', 'HIIT'),
        ('other', 'Other'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('hi', 'Hindi'),
        ('other', 'Other'),
    ]

    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    LOOKING_FOR = [
        ('partner', 'Workout Partner'),
        ('trainer', 'Trainer'),
        ('group', 'Group'),
    ]

    PARTNER_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    bio = models.TextField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)  # e.g., specific address or gym name
    preferred_workout = MultiSelectField(choices=WORKOUT_CHOICES, blank=True)
    preferred_language = MultiSelectField(choices=LANGUAGE_CHOICES, blank=True)
    available_days = MultiSelectField(choices=DAY_CHOICES, blank=True)
    training_time = MultiSelectField(choices=TIME_CHOICES, blank=True)
    looking_for = models.CharField(max_length=20, choices=LOOKING_FOR, blank=True)
    partner_level = models.CharField(max_length=20, choices=PARTNER_LEVEL, blank=True)
    running = models.PositiveIntegerField(null=True, blank=True)  # e.g., km per week
    gym = models.BooleanField(default=False)
    cycling = models.PositiveIntegerField(null=True, blank=True)  # e.g., km per week
    sports = models.TextField(max_length=200, blank=True)  # e.g., "tennis, basketball"
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    area = models.PositiveIntegerField(null=True, blank=True)  # e.g., search radius in km
    partner_age = models.PositiveIntegerField(null=True, blank=True)  # Preferred partner age
    
    def __str__(self):
        return f"Profile for {self.username}"

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.profile.username}"
