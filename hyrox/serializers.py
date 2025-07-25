# accounts/serializers.py
from datetime import timedelta
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, OTP
from django.utils import timezone
from .utils import generate_otp, MessageHandler

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    otp = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'confirm_password', 'first_name', 'last_name', 'otp']

    def validate(self, data):
        # Password matching
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # Password strength
        try:
            validate_password(data['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Check username/email uniqueness
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})

        # Validate OTP if provided
        if 'otp' in data:
            user = self.context.get('user')
            if not user:
                raise serializers.ValidationError({"otp": "User not found."})
            otp_obj = OTP.objects.filter(user=user, otp=data['otp'], is_verified=False).first()
            if not otp_obj:
                raise serializers.ValidationError({"otp": "Invalid OTP."})
            if otp_obj.is_expired():
                raise serializers.ValidationError({"otp": "OTP has expired."})

        return data

    def create(self, validated_data):
        # Remove confirm_password and otp
        validated_data.pop('confirm_password')
        validated_data.pop('otp', None)
        phone_number = validated_data.pop('phone_number', None)

        # Create User
        userpro = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        print(validated_data['first_name'])
        # Create UserProfile
        UserProfile.objects.create(
            user=userpro,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=phone_number
        )

        # Generate and send OTP
        otp = generate_otp()
        expires_at = timezone.now() + timedelta(minutes=5)
        OTP.objects.create(user=userpro, otp=otp, expires_at=expires_at)

        # Send OTP via email and SMS (if phone number provided)
        handler = MessageHandler(phone_number=phone_number, email=validated_data['email'], otp=otp)
        handler.send_otp_via_email()
        if phone_number:
            handler.send_otp_via_sms()

        return userpro