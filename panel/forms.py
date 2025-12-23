from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from main.models import Transaction

def validate_image_extension(value):
    valid_extensions = ["jpg", "jpeg", "png"]
    if "." not in value.name:
        raise ValidationError("فقط فرمت‌های JPG و PNG مجاز هستند.")
    
    ext = value.name.split(".")[-1].lower()

    if ext not in valid_extensions:
        raise ValidationError("فقط فرمت‌های JPG و PNG مجاز هستند.")

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["date"].initial = timezone.localtime().strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Transaction

        fields = ["transaction_type", "amount", "category", "comment", "date"]
        widgets = {
            "transaction_type": forms.RadioSelect(
                choices=Transaction.TRANSACTION_TYPES, 
                attrs={"class": "radio-option"}),
            "amount": forms.NumberInput(
                attrs={"placeholder": "مبلغ را وارد کنید", 
                       "id": "amount", 
                       "class": "form-control"}),
            "category": forms.Select(
                attrs={"id": "category", 
                       "class": "form-control"}),
            "comment": forms.TextInput(
                attrs={"placeholder": "توضیحات تراکنش (اختیاری)", 
                       "id": "description", 
                       "class": "form-control"}),
            "date": forms.DateTimeInput(
                attrs={"id": "date", 
                       "class": "form-control", 
                       "type": "datetime-local"}, 
                       format="%Y-%m-%dT%H:%M")
        }
        error_messages = {
            "transaction_type": {
                "required": "لطفا نوع تراکنش را انتخاب کنید.",
                "invalid_choice": "نوع تراکنش انتخاب شده معتبر نیست."
            },

            "amount": {
                "required": "لطفا مبلغ را وارد کنید.",
                "invalid": "مبلغ وارد شده معتبر نیست.",
                "min_value": "مبلغ نمی‌تواند کمتر از 0 باشد."
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

class EditProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"id": "name"}),
        error_messages={
            "required": "لطفا نام را وارد کنید."
        })
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"id": "last_name"}),
        error_messages={
            "required": "لطفا نام خانوادگی را وارد کنید."
        })


class EditAvatarForm(forms.Form):
    profile_picture = forms.FileField(
        validators=[validate_image_extension],
        widget=forms.FileInput(
            attrs={"accept": "image/*"}),
            error_messages={
            "required": "لطفا یک تصویر انتخاب کنید.",
            "invalid": "فقط فرمت‌های JPG و PNG مجاز هستند.",
            "invalid_image": "فایل انتخاب شده تصویر معتبر نیست.",
        })


    def clean_profile_picture(self):
        picture = self.cleaned_data.get("profile_picture")

        if picture:
            if picture.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("حجم عکس نباید بیشتر از ۲ مگابایت باشد.")

        return picture


class EditPasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "******", 
                    "id": "password", 
                    "name": "password"}),
        error_messages={
            "required": "لطفا رمز عبور را وارد کنید."
        })
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "******", 
                   "id": "confirm_password", 
                   "name":"password"}),
        error_messages={
            "required": "لطفا رمز عبور را وارد کنید."
        })
    
class FinancialTargetForm(forms.Form):
    financial_target_text = forms.CharField(
        max_length=250,
        widget=forms.Textarea(
            attrs={
                "placeholder": "قصد دارم طی ماه‌های آینده بخشی از درآمدم را برای سرمایه‌گذاری اختصاص دهم.",
                "class":"hadaf"
            }
        )
    )

    # def clean_text(self):
    #     text = self.cleaned_data["text"]
    #     if len(text) > 250:
    #         raise forms.ValidationError("حد اکثرکاراکتر مجاز 250 است.")
    #     return text