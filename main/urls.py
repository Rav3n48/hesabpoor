from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name="main-page"),
    path("login/", views.login_page, name="login-page"),
    path("signup/", views.signup_page, name="signup-page"),
    path("forgot_password/", views.forgot_password_page, name="forgot-password-page"),
    path("new_password/", views.password_reset_page, name="password-reset-page"),
    path("email/verify", views.verification_page, name="verification-page"),
    path("notification", views.notification_page, name="notification-page")
]
