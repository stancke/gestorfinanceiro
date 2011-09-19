# -*- coding: utf-8 -*- 
from gestao.models import Entrada, Saida
from django.contrib import admin

class EntradaAdmin(admin.ModelAdmin):
    
    list_display = ('tipo_de_entrada', 'titulo', 'descricao', 'valor', 'data_de_entrada')


admin.site.register(Entrada, EntradaAdmin)

class SaidaAdmin(admin.ModelAdmin):
    
    list_display = ('tipo_de_saida', 'titulo', 'descricao', 'valor','data_de_saida')
    

admin.site.register(Saida, SaidaAdmin)