from django.shortcuts import render
from .models import Account
from django.template.response import TemplateResponse
from django.views.generic import ListView

# Create your views here.
def account_tree_view(request):
    context = {
        'root_accounts': Account.objects.filter(parent = None),
    }
    return TemplateResponse(request, "account_tree_view.html", context)