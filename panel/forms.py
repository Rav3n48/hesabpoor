from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from . import models

User = get_user_model()


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ["transaction_type", "amount", "category", "comment", "date"]
        widgets = {
            "transaction_type": forms.RadioSelect(
                choices=models.Transaction.TRANSACTION_TYPES,
                attrs={
                    "class": "radio-option"
                }),
            "amount": forms.NumberInput(
                attrs={
                    "placeholder": "مبلغ را وارد کنید",
                    "id": "amount",
                    "class": "form-control"
                }),
            "category": forms.Select(
                attrs={
                    "id": "category",
                    "class": "form-control"
                }),
            "comment": forms.TextInput(
                attrs={
                    "placeholder": "توضیحات تراکنش (اختیاری)",
                    "id": "description",
                    "class": "form-control"
                }),
            "date": forms.DateTimeInput(
                attrs={
                    "id": "date",
                    "class": "form-control",
                    "type": "datetime-local"
                }
            )}
        error_messages = {
            "transaction_type": {
                "required": "لطفا نوع تراکنش را انتخاب کنید.",
                "invalid_choice": "نوع تراکنش انتخاب شده معتبر نیست."
            },

            "amount": {
                "required": "لطفا مبلغ را وارد کنید.",
                "invalid": "مبلغ وارد شده معتبر نیست.",
                "min_value": "مبلغ نمی‌تواند کمتر از ۰ باشد."
            },

            "category": {
                "required": "لطفا دسته‌بندی را مشخص کنید.",
                "invalid_choice": "دسته‌بندی انتخاب‌شده معتبر نیست."
            },

            "comment": {
                "max_length": "توضیحات بیش از حد طولانی است.",
                "invalid": "توضیحات وارد شده معتبر نیست.",
            },

            "date": {
                "required": "لطفا تاریخ را وارد کنید.",
                "invalid": "فرمت تاریخ معتبر نیست.",
            },
        }


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "name"
            }),
        error_messages={
            "required": "لطفا نام را وارد کنید.",
            "min_length": "نام نمی تواند کمتر از ۲ حرف باشد.",
            "max_length": "نام نمی تواند بیشتر از ۱۰۰ حرف باشد."
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "last_name"
            }),
        error_messages={
            "required": "لطفا نام خانوادگی را وارد کنید.",
            "min_length": "نام خانوادگی نمی تواند کمتر از ۲ حرف باشد.",
            "max_length": "نام خانوادگی نمی تواند بیشتر از ۱۰۰ حرف باشد."
        }
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class EditAvatarForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={"accept": "image/*"}),
        error_messages={
            "required": "لطفا یک تصویر انتخاب کنید."
        }
    )

    class Meta:
        model = models.Profile
        fields = ["profile_picture"]

    def clean_profile_picture(self):
        picture = self.cleaned_data.get("profile_picture")
        valid_extensions = ["jpg", "jpeg", "png"]
        if picture:
            if "." not in picture.name:
                raise ValidationError("فقط فرمت‌های JPG و PNG مجاز هستند.")

            ext = picture.name.split(".")[-1].lower()

            if ext not in valid_extensions:
                raise ValidationError("فقط فرمت‌های JPG و PNG مجاز هستند.")

            if picture.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("حجم عکس نباید بیشتر از ۲ مگابایت باشد.")

        return picture


class EditPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'رمز عبور فعلی',
                'class': 'form-control',
                'id': 'old_password',
            }),
        error_messages={
            'required': 'لطفا رمز عبور فعلی را وارد کنید.',
            "min_length": "رمز عبور نمی تواند کمتر از ۶ کاراکتر باشد.",
            "max_length": "رمز عبور نمی تواند بیشتر از ۱۲۸ کاراکتر باشد."
        }
    )

    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'رمز عبور جدید',
                'class': 'form-control',
                'id': 'new_password1',
            }),
        error_messages={
            'required': 'لطفا رمز عبور جدید را وارد کنید.',
            "min_length": "رمز عبور نمی تواند کمتر از ۶ کاراکتر باشد.",
            "max_length": "رمز عبور نمی تواند بیشتر از ۱۲۸ کاراکتر باشد."
        }
    )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'تکرار رمز عبور جدید',
                'class': 'form-control',
                'id': 'new_password2',
            }),
        error_messages={
            'required': 'لطفا تکرار رمز عبور جدید را وارد کنید.',
            "min_length": "رمز عبور نمی تواند کمتر از ۶ کاراکتر باشد.",
            "max_length": "رمز عبور نمی تواند بیشتر از ۱۲۸ کاراکتر باشد."
        }
    )


class FinancialTargetForm(forms.ModelForm):
    class Meta:
        model = models.FinancialTarget
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'قصد دارم طی ماه‌های آینده بخشی از درآمدم را برای سرمایه‌گذاری اختصاص دهم.',
                'class': 'hadaf',
            }),
        }
        error_messages = {
            'text': {
                'required': 'لطفا متن هدف مالی را وارد کنید.',
                'max_length': 'هدف مالی نمی‌تواند بیشتر از ۱۰۰ کاراکتر باشد.',
            },
        }
