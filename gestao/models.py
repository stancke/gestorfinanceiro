from django.db import models
from configuracao.models import TiposDeEntrada, TiposDeSaida


class Entrada(models.Model):
    
    tipo_de_entrada = models.ForeignKey(TiposDeEntrada)
    titulo = models.CharField(max_length=25)
    descricao = models.TextField(max_length=120)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_de_entrada = models.DateField(null=True)
    
    def __unicode__(self):
        return self.titulo
    
class Saida(models.Model):
    
    tipo_de_saida = models.ForeignKey(TiposDeSaida)
    titulo = models.CharField(max_length=25)
    descricao = models.TextField(max_length=120)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_de_saida = models.DateField(null=True)
    
    def __unicode__(self):
        return self.titulo