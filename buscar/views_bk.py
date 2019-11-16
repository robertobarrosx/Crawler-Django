from django.http import HttpResponse
from django.shortcuts import render
from buscar import busca


def index(request):

    search = request.GET.get('search')
    try:
        if search:
            link_acessados = busca.acessar_url(search)
            eita = busca.acessar(link_acessados)
        else:
            eita = []
    except:
        eita = None
    return render(request,'buscar.html',{'var':eita})
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")