from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.core.exceptions import ValidationError
from .models import Profile, ProfilePhoto
from multiselectfield import MultiSelectField
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        # Password confirmation
        if password != confirm:
            raise ValidationError("Passwords do not match.")

        # Password strength validation
        if len(password) < 8 or \
           not re.search(r"[A-Z]", password) or \
           not re.search(r"\d", password) or \
           not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must be at least 8 characters long and contain an uppercase letter, a number, and a special character.")

        return cleaned_data
# accounts/forms.py
class ProfileForm(forms.ModelForm):
    # Define multi-select fields without 'widget' or 'required' parameters
    preferred_workout = MultiSelectField(choices=Profile.WORKOUT_CHOICES)
    preferred_language = MultiSelectField(choices=Profile.LANGUAGE_CHOICES)
    available_days = MultiSelectField(choices=Profile.DAY_CHOICES)
    training_time = MultiSelectField(choices=Profile.TIME_CHOICES)
    # Multiple photos upload using FileInput
    uploaded_photos = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'full_name', 'username', 'bio', 'gender', 'age', 'country', 'state', 'city',
            'location', 'preferred_workout', 'preferred_language', 'available_days',
            'training_time', 'looking_for', 'partner_level', 'running', 'gym', 'cycling',
            'sports', 'profile_image', 'video', 'area', 'partner_age'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 13, 'max': 120}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_workout': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'preferred_language': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'available_days': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'training_time': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'looking_for': forms.Select(attrs={'class': 'form-select'}),
            'partner_level': forms.Select(attrs={'class': 'form-select'}),
            'running': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'min': 0, 'max': 100}),
            'gym': forms.CheckboxInput(),
            'cycling': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'min': 0, 'max': 100}),
            'sports': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'area': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'min': 0, 'max': 100}),
            'partner_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 13, 'max': 120}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.user.username:
            raise ValidationError("Username must match the authenticated user's username.")
        if Profile.objects.filter(username=username).exclude(user=self.user).exists():
            raise ValidationError("Username is already taken.")
        return username

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio and len(bio.split()) > 200:
            raise ValidationError("Bio must not exceed 200 words.")
        return bio

    def clean_age(self):
        age = self.cleaned_data['age']
        if age and (age < 13 or age > 120):
            raise ValidationError("Age must be between 13 and 120.")
        return age

    def clean_partner_age(self):
        partner_age = self.cleaned_data['partner_age']
        if partner_age and (partner_age < 13 or partner_age > 120):
            raise ValidationError("Partner age must be between 13 and 120.")
        return partner_age

    def clean_running(self):
        running = self.cleaned_data['running']
        if running is not None and (running < 0 or running > 100):
            raise ValidationError("Running must be between 0 and 100 km/week.")
        return running

    def clean_cycling(self):
        cycling = self.cleaned_data['cycling']
        if cycling is not None and (cycling < 0 or cycling > 100):
            raise ValidationError("Cycling must be between 0 and 100 km/week.")
        return cycling

    def clean_area(self):
        area = self.cleaned_data['area']
        if area is not None and (area < 0 or area > 100):
            raise ValidationError("Area must be between 0 and 100 km.")
        return area

    def clean_uploaded_photos(self):
        photos = self.files.getlist('uploaded_photos')
        for photo in photos:
            if not photo.content_type.startswith('image/'):
                raise ValidationError("All uploaded files must be images.")
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Each photo must be less than 5MB.")
        return photos

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
            # Handle multiple photos
            uploaded_photos = self.files.getlist('uploaded_photos')
            for photo in uploaded_photos:
                ProfilePhoto.objects.create(profile=profile, image=photo)
        return profile

