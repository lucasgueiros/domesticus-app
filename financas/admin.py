from django.contrib import admin
from .models import Account, Entry, Transaction
from django.urls import path
from django.template.response import TemplateResponse
from .views import saldos_view

# Register your models here.

# Accounts
class AccountAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('saldos/', saldos_view),
        ]
        return my_urls + urls

admin.site.register(Account, AccountAdmin)
admin.site.register(Entry)
admin.site.register(Transaction)