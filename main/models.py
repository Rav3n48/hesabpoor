from django.db import models
from django.utils import timezone
import uuid
import os

# Create your models here.


# Users Table
class User(models.Model):
    def profile_upload_path(instance, filename): # Generate random name for pf picture
        ext = filename.split('.')[-1]
        new_name = f"{uuid.uuid4()}.{ext}"
        return os.path.join("uploads/profile_pictures", new_name)

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    new_password_code = models.CharField(max_length=64, blank=True, null=True)
    new_password_code_sent_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_upload_path, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(
        default=None, null=True, blank=True)
    verification_code = models.CharField(max_length=64, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    financial_targets = models.JSONField(default=list, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=30, decimal_places=0, default=0)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
    


# Transactions Table
class Transaction(models.Model):

    TRANSACTION_TYPES = (("income", "درآمد"), ("outcome", "هزینه"))
    CATEGORIES = (("nothing", "دسته بندی نشده"), ("salary", "حقوق"), ("food", "خوراک"), ("clothes","پوشاک"), 
                  ("transportation", "حمل و نقل"), ("hobby", "سرگرمی و تفریح"), ("health", "سلامتی"), 
                  ("investment", "سرمایه گذاری"), ("loan", "وام"), ("rent", "اجاره"), ("bill", "قبض ها"))
    
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name="transactions")
    category = models.CharField(max_length=20, default="nothing", choices=CATEGORIES, null=False, blank=False)
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, default="income", choices=TRANSACTION_TYPES, null=False, blank=False)
    comment = models.TextField(null=True, blank=True, max_length=250)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.transaction_type == True:
            type = "income"
        else:
            type = "outcome"

        return f"{self.amount} :{type}"
