# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import OTP,User
from .utils import generate_otp, MessageHandler
from django.utils import timezone
from datetime import timedelta

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "OTP sent to your email and/or phone. Please verify to complete registration.",
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        if not user_id or not otp:
            return Response({"error": "User ID and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegistrationSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            otp_obj = OTP.objects.filter(user=user, otp=otp, is_verified=False).first()
            if otp_obj:
                otp_obj.is_verified = True
                otp_obj.save()
                return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check rate limit manually (in addition to AnonRateThrottle)
        last_otp = OTP.objects.filter(user=user).order_by('-created_at').first()
        if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 60:
            return Response({"error": "Please wait before requesting a new OTP."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Generate and send new OTP
        otp = generate_otp()
        expires_at = timezone.now() + timedelta(minutes=5)
        OTP.objects.create(user=user, otp=otp, expires_at=expires_at)

        handler = MessageHandler(phone_number=user.profile.phone_number, email=user.email, otp=otp)
        handler.send_otp_via_email()
        if user.profile.phone_number:
            handler.send_otp_via_sms()

        return Response({"message": "New OTP sent."}, status=status.HTTP_200_OK)