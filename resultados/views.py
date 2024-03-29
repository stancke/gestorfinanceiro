from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from gestao.models import Entrada, Saida


def index(request):

    if request.user.is_authenticated():

        return render_to_response('resultados/index.html')
    else:
        return HttpResponseRedirect("/erro_autenticacao/")
    
def resultados(request, url):

    if request.user.is_authenticated():

        return render_to_response('resultados/resultados.html')
    else:
        return HttpResponseRedirect("/erro_autenticacao/")
    

def getAllSaidas(request):
    saidas = Saida.objects.values('tipo_de_saida').distinct()
    
    return HttpResponse(saidas)