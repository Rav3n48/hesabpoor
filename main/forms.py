from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا نام خود را وارد کنید.',
            "min_length": "نام نمی تواند کمتر از ۲ حرف باشد.",
            "max_length": "نام نمی تواند بیشتر از ۱۰۰ حرف باشد."
        })
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا نام  خود را وارد کنید.',
            "min_length": "نام خانوادگی نمی تواند کمتر از ۲ حرف باشد.",
            "max_length": "نام خانوادگی نمی تواند بیشتر از ۱۰۰ حرف باشد."
        })
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا ایمیل را وارد کنید.',
            'invalid': 'ایمیل وارد شده معتبر نیست.',
            'unique': 'مشکلی در ثبت نام به وجود آمده. لطفا در وارد کردن اطلاعات خود دقت کنید یا اگر قبلا ثبت نام کرده اید از صفحه ورود اقدام کنید.'
        })
    password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا رمز عبور را وارد کنید.'
        })
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا تایید رمز عبور را وارد کنید.'
        })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید.',
            'invalid': 'لطفا ایمیل معتبر وارد کنید.'
        }
    )
    error_messages = {
        "invalid_login": "لطفا ایمیل و رمز عبور معتبر وارد کنید."
    }

    class Meta:
        model = User
        fields = ['username', 'password']
