from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import os
import uuid

User = get_user_model()


def get_profile_upload_path(instance, filename):  # Generate random name for pf picture
    ext = os.path.splitext(filename)[1]
    new_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/profile_pictures', new_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=get_profile_upload_path, null=True, blank=True)
    balance = models.DecimalField(max_digits=30, decimal_places=0, default=0)


class FinancialTarget(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='financial_targets')


class Transaction(models.Model):
    TRANSACTION_TYPES = (('income', 'درآمد'), ('outcome', 'هزینه'))
    CATEGORIES = (('nothing', 'دسته بندی نشده'), ('salary', 'حقوق'), ('food', 'خوراک'), ('clothes', 'پوشاک'),
                  ('transportation', 'حمل و نقل'), ('hobby', 'سرگرمی و تفریح'), ('health', 'سلامتی'),
                  ('investment', 'سرمایه گذاری'), ('loan', 'وام'), ('rent', 'اجاره'), ('bill', 'قبض ها'))

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    category = models.CharField(max_length=20, default='nothing', choices=CATEGORIES, null=False, blank=False)
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, default='income', choices=TRANSACTION_TYPES, null=False,
                                        blank=False)
    comment = models.TextField(null=True, blank=True, max_length=250)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.transaction_type:
            tr_type = 'income'
        else:
            tr_type = 'outcome'

        return f'{self.amount} :{tr_type}'
