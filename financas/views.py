from django.shortcuts import render
from .models import Account
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Create your views here.
def account_tree_view(request):
    context = {
        'root_accounts': Account.objects.filter(parent = None),
    }
    return TemplateResponse(request, "account_tree_view.html", context)

class AccountDetailView(DetailView):
    model = Account
    template_name = "account_detail_view.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saldo = 0
        entries = []
        for entry in self.get_object().entries.order_by('transaction__date').all():
            saldo = saldo + entry.amount
            
            # Encontrando a outra conta...
            other_entries = entry.transaction.entries.filter(~Q(id=entry.id)).all()
            other_entry = other_entries.first()
            more_entries =  len(other_entries) > 0
            
            entries.append( (entry, saldo, other_entry, more_entries) )
        context["entries"] = entries
        return context
        