from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import SendFund, RequestFund, Balance



class CustomUserAdmin(UserAdmin):
    list_display = ("first_name", "last_name", "username", "email", "balance", "is_staff", "last_login")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name", "balance")
    ordering = ("username", "first_name", "last_name")


class SendFundAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "sender_currency", "receiver_currency",
                    "amount", "quote_amount", "sender_balance_amount", "receiver_balance_amount",
                    "date")
    list_filter = ("sender_currency", "receiver_currency")
    search_fields = ("sender", "receiver", "sender_currency", "receiver_currency")
    ordering = ("date",)



class RequestFundAdmin(admin.ModelAdmin):
    list_display = ("requester", "funder", "amount", "currency", "status", "date")
    list_filter = ("status", "currency")
    search_fields = ("sender", "receiver", "sender_currency", "receiver_currency")
    ordering = ("date",)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "currency")
    list_filter = ("currency",)
    search_fields = ("user", "currency")
    ordering = ("user",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(SendFund, SendFundAdmin)
admin.site.register(RequestFund, RequestFundAdmin)
admin.site.register(Balance, BalanceAdmin)


