from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    GoogleLoginSerializer,
    RegisterSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    OTPLoginSerializer,
    OTPVerifySerializer,
)
from core.settings import EMAIL_CONFIRM_REDIRECT_BASE_URL, PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/api/auth/callback/google"
    client_class = OAuth2Client

    @swagger_auto_schema(request_body=GoogleLoginSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OTPLoginView(APIView):
    @swagger_auto_schema(request_body=OTPLoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            device = EmailDevice.objects.filter(user=user).first()
            if not device:
                device = EmailDevice.objects.create(user=user, email=email)

            device.generate_challenge()
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {device.token}",
                "gopalkr022@gmail.com",
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

        return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    @swagger_auto_schema(request_body=OTPVerifySerializer)
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        user = User.objects.filter(email=email).first()

        if user:
            device = EmailDevice.objects.filter(user=user).first()
            if device and device.verify_token(otp):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
