from django.contrib import admin
from .models import User, Transaction

# Register your models here.

#register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "balance", "email_verified", "is_deleted")
    list_filter = ("is_deleted", "email_verified")
    search_fields = ("full_name", "email")

#register Transaction model
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user_id", "amount", "transaction_type")
    list_filter = ("transaction_type", "category")
