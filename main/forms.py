from django import forms


class UserSignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا نام را وارد کنید."
        })
    last_name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا نام خانوادگی را وارد کنید."
        })
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا ایمیل را وارد کنید.",
            "invalid": "ایمیل وارد شده معتبر نیست."
        })
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا رمز عبور را وارد کنید."
        })


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا ایمیل را وارد کنید.",
            "invalid": "ایمیل وارد شده معتبر نیست."
        })
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا رمز عبور را وارد کنید."
        })


class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا ایمیل را وارد کنید.",
            "invalid": "ایمیل وارد شده معتبر نیست."
        })


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": ""}),
        error_messages={
            "required": "لطفا رمز عبور را وارد کنید."
        })
