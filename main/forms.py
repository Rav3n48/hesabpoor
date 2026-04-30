from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا نام را وارد کنید.'
        })
    last_name = forms.CharField(
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا نام خانوادگی را وارد کنید.'
        })
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': ''}),
        error_messages={
            'required': 'لطفا ایمیل را وارد کنید.',
            'invalid': 'ایمیل وارد شده معتبر نیست.'
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
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user
