from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
import secrets

from .email_sender import send_verify_code, send_password_code
from .models import User
from .forms import UserSignUpForm, UserLoginForm, EmailForm, PasswordResetForm
from .password_hasher import hash_password, verify_password


def main_page(request):
    return render(request, "main/landing.html")


def login_page(request):
    user_id = request.session.get("user_id")
    if user_id:  # if already was logged in don't show login-page
        return redirect("panel-page")
    
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "main/login.html", {"form": form})
    
    elif request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Form is valid
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.filter(email=email).first()  # Find the user

            if not user:  # User not found
                form.add_error(
                    "email", "ایمیل یا رمز عبور وارد شده اشتباه است.")
                return render(request, "main/login.html",
                              {"form": form})

            if not verify_password(password, user.password):  # Wrong password
                form.add_error("password", "ایمیل یا رمز عبور وارد شده اشتباه است.")
                return render(request, "main/login.html",
                              {"form": form})
            
            if not user.email_verified:
                form.add_error("email", "لطفا ابتدا ایمیل خود را تایید کنید.")
                return render(request, "main/login.html",
                              {"form": form})


            # Login success
            request.session["user_id"] = user.id  # save cookie
            return redirect("panel-page")

        # Form not valid
        return render(request, "main/login.html", {"form": form})


def signup_page(request):
    user_id = request.session.get("user_id")
    if user_id:  # if already was logged in don't show signup-page
        return redirect("panel-page")
    
    if request.method == "GET":
        form = UserSignUpForm()
        return render(request, "main/signup.html", {"form": form})
    
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = hash_password(form.cleaned_data["password"])


            if len(form.cleaned_data["password"]) < 6:  # Password 6 character
                form.add_error(
                    "password", "رمز عبور حداقل باید ۶ کاراکتر باشد.")
                return render(request, "main/signup.html",
                              {"form": form})

            user = User.objects.filter(email=email).first()

            if user:
                request.session["notification_code"] = 8 # Misleading error
                request.session["extra"] = True
                request.session["extra_url"] = "signup-page"
                request.session["extra_text"] = "ثبت نام"
                return redirect("notification-page")

            # Generate random code with 48 character and url-safe
            verify_code = secrets.token_urlsafe(48)

            # Create a new user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                verification_code=verify_code,
                email_verification_sent_at=timezone.now()
            )

            send_verify_code(request, user)
            request.session["notification_code"] = 1
            request.session["extra"] = False
            return redirect("notification-page")

        # Form not valid
        return render(request, "main/signup.html", {"form": form})



def verification_page(request):
    user_id = request.session.get("user_id")
    if user_id:  # if already was logged in don't show verification-page
        return redirect("panel-page")
    
    if request.method == "GET":
        code = request.GET.get("vcode") # get code from link which was sent by email

        if not code or code == "verified": # check if code is valid
            request.session["notification_code"] = 2
            request.session["extra"] = False
            return redirect("notification-page")
    
        # Try to find which user that code belongs to
        try: 
            user = User.objects.get(verification_code=code) 
        except User.DoesNotExist:
            request.session["notification_code"] = 2
            request.session["extra"] = False
            return redirect("notification-page")

        expiration_time = user.email_verification_sent_at + timedelta(minutes=30) 

        if timezone.now() > expiration_time: # Check if the code has expired
            user.delete()
            request.session["notification_code"] = 3
            request.session["extra"] = True
            request.session["extra_url"] = "signup-page"
            request.session["extra_text"] = "ثبت نام"
            return redirect("notification-page")
    
        # verification success
        user.email_verified = True
        user.email_verified_at = timezone.now()
        user.verification_code = "verified"
        user.save()

        # Sign up success
        request.session["user_id"] = user.id
        request.session["notification_code"] = 4
        request.session["extra"] = True
        request.session["extra_url"] = "panel-page"
        request.session["extra_text"] = "ورود به پنل"
        return redirect("notification-page")


def forgot_password_page(request):
    user_id = request.session.get("user_id")
    if user_id:  # if already was logged in don't show forgot-password-page
        return redirect("panel-page")
    
    if request.method == "GET":
        # Get request
        form = EmailForm()
        return render(request, "main/forgot_password.html", {"form": form})
    
    elif request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.filter(email=email).first() # Find user with email

            if not user:  # User doesn't exist
                request.session["notification_code"] = 5 # Fake error
                request.session["extra"] = False
                return redirect("notification-page")

            new_password_code = secrets.token_urlsafe(48)
            user.new_password_code = new_password_code
            user.new_password_code_sent_at = timezone.now()
            user.save()

            send_password_code(request, user)

            request.session["notification_code"] = 5
            request.session["extra"] = False
            return redirect("notification-page")



def password_reset_page(request):
    user_id = request.session.get("user_id")
    if user_id:  # if already was logged in don't show password-reset-page
        return redirect("panel-page")

    if request.method == "GET":
        # Get request
        code = request.GET.get("rcode")

        if not code:
            request.session["notification_code"] = 2
            request.session["extra"] = False
            return redirect("notification-page")
        
        try:
            user = User.objects.get(new_password_code=code)
        except User.DoesNotExist:
            request.session["notification_code"] = 2
            request.session["extra"] = False
            return redirect("notification-page")

        expiration_time = user.new_password_code_sent_at + timedelta(minutes=30)

        if timezone.now() > expiration_time:
            user.new_password_code = None
            user.save()
            request.session["notification_code"] = 6
            request.session["extra"] = True
            request.session["extra_url"] = "forgot-password-page"
            request.session["extra_text"] = "فراموشی رمز"
            return redirect("notification-page")

        form = PasswordResetForm()
        return render(request, "main/new_password.html", {"form": form, })

    elif request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            code = request.POST.get("rcode")

            if not code:
                request.session["notification_code"] = 2
                request.session["extra"] = False
                return redirect("notification-page")

            try:
                user = User.objects.get(new_password_code=code)
            except User.DoesNotExist:
                request.session["notification_code"] = 2
                request.session["extra"] = False
                return redirect("notification-page")

            expiration_time = user.new_password_code_sent_at + timedelta(minutes=30)

            if timezone.now() > expiration_time:
                user.new_password_code = None
                user.save()
                request.session["notification_code"] = 6
                request.session["extra"] = False
                return redirect("notification-page")

            if len(form.cleaned_data["password"]) < 6:  # Password 6 character
                form.add_error(
                    "password", "رمز عبور حداقل باید ۶ کاراکتر باشد.")
                return render(request, "main/new_password.html",
                              {"form": form})

            user.password = hash_password(password)
            user.new_password_code = None
            user.save()

            request.session["notification_code"] = 7
            request.session["extra"] = True
            request.session["extra_url"] = "login-page"
            request.session["extra_text"] = "صفحه لاگین"
            return redirect("notification-page")

        else:
            return render(request, "main/new_password.html", {"form": form})


def notification_page(request):
    if request.method == "GET":
        context = {
        "notification_code": request.session.get("notification_code"),
        "extra": request.session.get("extra"),
        "extra_url": request.session.get("extra_url"),
        "extra_text": request.session.get("extra_text"),
        }

        # Clear session values AFTER copying them
        request.session["notification_code"] = None
        request.session["extra"] = None
        request.session["extra_url"] = None
        request.session["extra_text"] = None

        return render(request, "main/notification.html", context)
