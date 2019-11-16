from django.http import HttpResponse
from django.shortcuts import render
from buscar import busca_thread
from buscar import busca_bk

def index(request):
    search = request.GET.get('search')
    if search:
        recurso = []
        aux = []
        result = []
        url = search
        recurso.append(url)
        inicio = busca_thread.time.time()
        final = round(busca_thread.time.time() - inicio, 2)
        while len(recurso) > 0 and final < 60:
            final = round(busca_thread.time.time() - inicio, 2)
            try:
                if search:
                    dominio = busca_thread.definirDominio(url)
                    rlock = busca_thread.RLock()
                    t = []
                    for i in range(5):
                        t.append(busca_thread.Desapegadora(rlock, recurso, result, dominio,aux))
                        t[i].start()
                    final = round(busca_thread.time.time() - inicio, 2)
                    if(final > 60):
                        for i in t:
                            i.stop()
                    for i in t:
                        i.join()

                else:
                    result = []
            except:
                y = None


        final = round(busca_thread.time.time() - inicio, 2)
        print(f"Tempo de execução: {final} s\nRecursos: {len(recurso)}")
    else:
        result = []
        final = 0

    return render(request,'buscar.html',{'var':result,'tempo':final})
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index2(request):

    search = request.GET.get('search')
    eita = []

    final = 0
    if search:
        eita.append(busca_bk.acessar_url(search))
    else:
        eita = []
    try:
        inicio = busca_bk.time.time()
        if search:
            link_acessados = busca_bk.acessar_url(search)
            eita = busca_bk.acessar(link_acessados)
        else:
            eita = []
        final = round(busca_bk.time.time() - inicio, 2)
        print(f"Tempo de execução: {final} s")
    except:
        eita = None
        final = 0

    print(final)
    return render(request,'buscar.html',{'var':eita,'tempo':final})