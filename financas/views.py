from django.shortcuts import render
from .models import Account
from django.template.response import TemplateResponse

# Create your views here.
def saldos_view(request):
    context = {
        'accounts': Account.objects.all(),
    }
    return TemplateResponse(request, "saldos.html", context)