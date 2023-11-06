from django.contrib import admin

from .models import Accounts
# Register your models here.

class showAccounts(admin.ModelAdmin):
    list_display=["user","date","reason","amount"]

admin.site.register(Accounts, showAccounts)