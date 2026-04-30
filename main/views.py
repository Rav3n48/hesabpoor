from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils import timezone


from .models import User
from .forms import UserSignUpForm


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        base = super()._make_hash_value(user, timestamp)
        return f'email_verify{base}'


email_verification_token_generator = EmailVerificationTokenGenerator()


class IndexView(View):
    def get(self, request):
        return render(request, 'main/landing.html')


class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('panel-page')
        form = UserSignUpForm()
        return render(request, 'main/signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseBadRequest('شما هم اکنون وارد اکانت خودتان شدید و نمیتوانید ثبت نام کنید.')
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = email_verification_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            link = request.build_absolute_uri(reverse('verify_email', kwargs={'uidb64': uid, 'token': token}))
            send_mail(
                subject='حساب خود را تایید کنید',
                message=f'لطفا برای تایید حساب کاربری خود در وبسایت حساب پور  روی لینک زیر کلیک کنید:\n\n{link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            return render(request, 'main/email_verification_sent.html')
        return render(request, 'main/signup.html', {'form': form})


class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and email_verification_token_generator.check_token(user, token):
            user.is_active = True
            user.email_verified = True
            user.email_verified_at = timezone.now()
            user.save()
            return render(request, 'main/email_verification_done.html')
        return render(request, 'main/email_verification_error.html')
