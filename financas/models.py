from django.db import models

# Create your models here.
class Conta(model.Models):
    nome = models.TextField(max_length=100)
    mae = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='filhas',
    )

class Transacao(models.Model):
    pass

class Entrada(models.Model):
    pass