# -*- coding: utf-8 -*- 
from configuracao.models import TiposDeEntrada, TiposDeSaida
from django.contrib import admin

#class TiposDeEntradasAdmin(admin.ModelAdmin):
    
    #list_display = ('titulo')


admin.site.register(TiposDeEntrada)

#class TiposDeSaidasAdmin(admin.ModelAdmin):
    
    #list_display = ('titulo')


admin.site.register(TiposDeSaida)