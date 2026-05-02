from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_done.html'), name='password_reset_complete'),
    path('email/verify/<uidb64>/<token>/', views.EmailVerificationView.as_view(), name='email_verify'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
