from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
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
        if self.parent:
            return self.parent.__str__() + ":" + self.name
        else:
            return self.name
        

class Transaction(models.Model):
    date = models.DateTimeField()
    description = models.CharField(max_length=300)

    @property
    def saldo (self):
        saldo = 0
        for entry in self.entries.all():
            saldo = saldo + entry.amount
        return saldo

    def __str__(self):
        return self.description[:25]

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
    description = models.CharField(max_length=500)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    
    def __str__(self):
        return self.description