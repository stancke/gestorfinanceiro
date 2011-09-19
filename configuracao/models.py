from django.db import models

class TiposDeEntrada(models.Model):

    titulo = models.CharField(max_length=25)
    
    def __unicode__(self):
        return self.titulo
    
class TiposDeSaida(models.Model):

    titulo = models.CharField(max_length=25)
    
    def __unicode__(self):
        return self.titulo