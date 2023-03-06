from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    mother = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
    )
    
    def saldo (self):
        saldo = 0
        for entry in self.entries.all():
            saldo = saldo + entry.amount
        return saldo
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    data = models.DateTimeField()
    description = models.CharField(max_length=300)
    
    def __str__(self):
        return self.description

class Entry(models.Model):
    account = models.ForeignKey(
        Account,
        null=False,
        on_delete=models.CASCADE,
        related_name='entries',
    )
    transaction = models.ForeignKey(
        Transaction,
        null=True,
        on_delete=models.SET_NULL,
        related_name="entries",
    )
    description = models.CharField(max_length=100)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    
    def __str__(self):
        return self.description