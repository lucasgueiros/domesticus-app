from django.contrib import admin
from .models import Account, Entry, Transaction
from django.urls import path
from django.template.response import TemplateResponse
from .views import account_tree_view

# Register your models here.

class AccountEntriesAdminInline (admin.TabularInline):
    model = Entry
    fields = ('transaction','description', 'amount')

# Accounts
class AccountAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'parent',
        'saldo',
    )
    readonly_fields = (
        'saldo',
    )
    inlines = ( 
               AccountEntriesAdminInline,
    )
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('list/', account_tree_view),
        ]
        return my_urls + urls

class TransactionEntriesAdminInline (admin.TabularInline):
    model = Entry
    fields = ('account','description', 'amount')


class TransactionAdmin (admin.ModelAdmin):
    inlines = (
        TransactionEntriesAdminInline,
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(Entry)
admin.site.register(Transaction, TransactionAdmin)