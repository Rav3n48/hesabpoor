from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail


def send_verify_code(request, user):
    verify_url = request.build_absolute_uri(
        reverse("verification-page") + f"?vcode={user.verification_code}"
    )
    send_mail(
        subject="حساب خود را تایید کنید",
        message=f"لطفا برای تایید حساب کاربری خود در وبسایت حساب پور  روی لینک زیر کلیک کنید:\n\n{verify_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def send_password_code(request, user):
    new_password_url = request.build_absolute_uri(
        reverse("password-reset-page") + f"?rcode={user.new_password_code}"
    )

    send_mail(
        subject="تغییر رمز عبور",
        message=f"لطفا برای تغییر رمز عبور حساب کاربری خود در وبسایت حساب پور  روی لینک زیر کلیک کنید:\n\n{new_password_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
