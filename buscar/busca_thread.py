from threading import Thread, RLock
from urllib.request import Request, urlopen
import time

def verify_url(url):
    auxiliares = url.split("/")
    for i in auxiliares:
        if auxiliares.count(i) > 2:
            return False
    if len(url) < 9:
        return False
    if len(url) > 250:
        return False
    return True

def converter_link(url,continua):
    dominio = definirDominio_http(url)
    auxiliar = url + continua
    convertido = True
    #print(continua)
    if "mailto" in continua:
        if verify_url(continua):
            return continua
    if url.count("http") >= 2 or continua.count("http") >= 2:
        return "referenciando outro site"
    if "http" in continua[0:6]:
        # print("entrou http inicio")
        if verify_url(continua):
            return continua
    if "//" in continua[0:2]:
        # print("entrou // inicio")
        if verify_url(continua):
            return "http:"+continua
    # if(len(auxiliar) > 400):
    #     print("entrou url > 400")
    #     #print(len(auxiliar))
    #     convertido = False
    if continua.count("http") >= 2:
        # print("entrou http >=2")
        convertido = False
    if continua in url:
        # print("entrou continua in url")
        return url
    # if ";" in continua:
    #     print("entrou ; no continua")
    #     convertido = False


    if ".php" in url or ("?" in url and "=" in url):
        for i in range(len(url)-1,0,-1):
            if url[i] == "/":
                posicao = i
                break
        url = url[0:posicao]
        convertido = True

    if url[len(url) - 1] == "/":
            url = url[0:len(url) - 1]
    while "../" in continua:
        continua = continua.replace("../","",1)
        posicao = len(url)+1
        for i in range(len(url)-1,0,-1):
            if url[i] == "/":
                posicao = i
                break
        url = url[0:posicao]
    if continua[0] == "/":
        continua = continua[1:len(continua) + 1]
    url_final = url +'/'+ continua

    if (dominio in url_final) == False:
        # print("dominuo na url")
        return "wsdbsadm"
    if url_final.count("http") >= 2:
        # print("dominuo dois http na url")
        return "referenciando outro site"
    if verify_url(url_final) and convertido:
        # print(f"passou no verift - {url_final}")
        return url_final
    else:
        # print("não passou no verify")
        return "qualquermerda"


def definirDominio(url):
    dominio = url.replace("https://www.", "").replace("http://www.", "").replace("https://", "").replace("http://", "")
    if "/" in dominio:
        dominioAux = ""
        for i in dominio:
            if i == "/":
                break
            dominioAux += i
        return dominioAux
    return dominio

def definirDominio_http (url):
    dominio = url
    if "/" in dominio:
        dominioAux = ""
        for i,character in enumerate(dominio):
            if character == "/" and i > 7:
                break
            dominioAux += character
        return dominioAux
    return dominio
def ler_linhas(string):
    str = string.split("\n")
    return str;

def buscar_tags(linhas):
    tags=[]
    tagsAux = []
    validos = "abcdefghijklmnopqrstuvxzwy0123456789"
    invalid = " >()[]{}_"

    for i, linha in enumerate(linhas):
        while "<" in linha:
            posicao = linha.find('<')
            tag = ""
            pode = True
            for percorrer in range(posicao+1,len(linha)):
                if linha[percorrer] in invalid:
                    break
                if "!--" in tag:
                    tag = "!--"
                    break
                tag += linha[percorrer]
            for x in tag:
                if (x in validos) == False:
                    pode = False
                    break
            if (tag != "" and ("!" in tag) != True and ("/" in tag) != True) and pode or ("!doctype" in tag.lower() or "!--" == tag):
                tags.append(f"<{tag.rstrip()}>")
            linha = linha.replace(f"<{tag}","",1)

    for t in tags:
        tg = (t, tags.count(t))
        podeAdd = True
        for ta in tagsAux:
            if ta == tg:
                podeAdd = False
                break
        if podeAdd:
            tagsAux.append(tg)
    return tagsAux;
def buscar_links(linhas,url):
    links = []
    for i, linha in enumerate(linhas):
        while "href=\"" in linha or "src=\"" in linha or "href=\'" in linha or "src=\'" in linha:
            podeAdicionar = True
            posicao = linha.find('href=\"')
            if posicao < 0:
                posicao = linha.find('src=\"')
                if posicao < 0:
                    posicao = linha.find('src=\'')
                    if posicao < 0:
                        posicao = linha.find('href=\'')
                        if posicao > 0:
                            linha = linha.replace(f"href=\'", "", 1)
                    else:
                        linha = linha.replace(f"src=\'", "", 1)
                else:
                    linha = linha.replace(f"src=\"", "", 1)
            else:
                linha = linha.replace(f"href=\"", "", 1)
            x = posicao
            link = ""
            for percorrer in range(x, len(linha)):
                if (linha[percorrer] == "\"" or linha[percorrer] == "\'" or linha[percorrer] == "#"  \
                        or linha[percorrer] == " " or linha[percorrer] == "\\"):
                    break
                link += linha[percorrer]

            link = converter_link(url,link)
            for esy in links:
                    if esy.replace("/", "") == link.replace("/", ""):
                        podeAdicionar = False
                        # print("-------------------  Não passou dos já add -------------------")
                        continue
            if " " in link:
                podeAdicionar = False
                # print("-------------------  Não passou do primeiro if -------------------")
                continue
            if ("http" in link or "mailto" in link) == False :  #or ":" in link or ";" in link
                # print("-------------------  Não passou do segundo if -------------------")
                podeAdicionar = False
                continue
            #print("------------------------------------- FIM --------------------------------------------------")
            #print(link,podeAdicionar)
            if link != "" and podeAdicionar:
                # print("-------------------  Não entrou no if -------------------")
                if link[len(link)-1] == "/":
                    link = link[0:len(link)-1]
                links.append(link.rstrip())
           # print(link)
        # while "http:" in linha or "https:" in linha:
        #     posicao = linha.find('http')
        #     link = ""
        #     for percorrer in range(posicao, len(linha)):
        #         if (linha[percorrer] == "\"" or linha[percorrer] == "\'" or linha[percorrer] == "#" \
        #                 or linha[percorrer] == ")" or linha[percorrer] == " "):
        #             break
        #         link += linha[percorrer]
        #     aux = link
        #     link = link.replace("\\", "")
        #     for esy in links:
        #         if esy.replace("/", "") == link.replace("/", ""):
        #             podeAdicionar = False
        #     if "http" in link == False or "://" in link == False or len(link) < 10:
        #         podeAdicionar = False
        #     if link != "" and podeAdicionar:
        #         if link[len(link) - 1] == "/":
        #             link = link[0:len(link) - 1]
        #         links.append(link)
        #     linha = linha.replace(f"{aux}", "", 1)
    return links
def filtrar_links(links,dominio):
    filtro = []
    for link in links:
        i = link.find(dominio)
        podeAdd = True
        for pop in filtro:
            if pop == link:
                podeAdd = False
        if i > 0 and i < 20 and podeAdd:
            filtro.append(link)
    return filtro

def acessar_url(url):
    try:
        acessei = []
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        web_byte = urlopen(req).read()
        # try:
        #     webpage = web_byte.decode('utf-8')
        # except:
        #     try:
        #         webpage = web_byte.decode('latin-1')
        #     except:
        #         webpage = web_byte.decode('iso-8859-1')
        webpage = f"{web_byte}"
        acessei.append(url)
        linhas = ler_linhas(webpage)
        #print(linhas)
        todos_links = buscar_links(linhas,url)
        todas_tags = buscar_tags(linhas)
        return (url, todas_tags, todos_links)
    except:
        return None

def acessar(link):
    acessei = []
    acessei.append(link[0])
    dominio = definirDominio(link[0])
    filtrado = filtrar_links(link[2], dominio)
    link_acessados =[]
    links_para_acessar = []
    link_acessados.append((link[0], link[1], link[2]))
    links_arquivos = []
    for i in filtrado:
        links_para_acessar.append(i)
    while len(links_para_acessar) > 0:
        if len(links_para_acessar) < 1:
            break
        try:
            while ".zip" in links_para_acessar[0][len(links_para_acessar[0]) - 5:len(links_para_acessar[0])] or ".pdf" in \
                    links_para_acessar[0][len(links_para_acessar[0]) - 5:len(links_para_acessar[0])] or ".jpg" in \
                    links_para_acessar[0][len(links_para_acessar[0]) - 5:len(links_para_acessar[0])] \
                    or ".js" in links_para_acessar[0][len(links_para_acessar[0]) - 4:len(links_para_acessar[0])] :
                links_arquivos.append(links_para_acessar[0])
                links_para_acessar.remove(links_para_acessar[0])
        except:
            break

        if len(links_para_acessar) < 1:
            break

        url = links_para_acessar[0]

        # print(f"Numero de links para acessar: {len(links_para_acessar)}")
        # print(f"Numero de links validos: {len(link_acessados)}")
        # print(f"Numero de links acessados: {len(acessei)}")
        # print(url)
        links_para_acessar.remove(links_para_acessar[0])
        try:
            acessei.append(url)
            link_acessado = acessar_url(url)
            dominio = definirDominio(url)
            filtrado = filtrar_links(link_acessado[2], dominio)
            if len(link_acessado[1]) > 0:  #and len(link_acessado[2]) > 0:
                link_acessados.append((url, link_acessado[1], link_acessado[2]))
            else:
                links_arquivos.append(url)
            for f in filtrado:
                podeEntrar = True
                for lin in acessei:
                    if f == lin:
                        podeEntrar = False
                for low in links_para_acessar:
                    if low == f:
                        podeEntrar = False

                if ".zip" in f[len(f) - 5:len(f)] or ".pdf" in f[len(f) - 5:len(f)] or ".jpg" in f[len(f) - 5:len(f)] or ".c" in f[len(f) - 3:len(f)] \
                    or ".doc" in f[len(f) - 5:len(f)] or ".rar" in f[len(f) - 5:len(f)] or \
                        ".png" in f[len(f) - 5:len(f)] or ".gif" in f[len(f) - 5:len(f)] \
                        or ".txt" in f[len(f) - 5:len(f)] or ".js" in f[len(f) - 4:len(f)]:
                    links_arquivos.append(f)
                    podeEntrar = False
                if podeEntrar:
                    links_para_acessar.append(f)
        except:
            links_arquivos.append(url)
    return link_acessados

class Acumuladora(Thread):

    def __init__(self, rlock, recurso):
        Thread.__init__(self)
        self.rlock = rlock
        self.recurso = recurso

    def acumula(self):
        self.rlock.acquire()
        ####regiao critica
        self.recurso[0] += 1
        ###fim da regiao critica
        self.rlock.release()

    def run(self):
        for i in range(20):
            self.rlock.acquire()
            self.acumula()
            self.rlock.release()


class Desapegadora(Thread):

    def __init__(self, rlock,recurso,result,dominio,acessados):
        Thread.__init__(self)
        self.rlock = rlock
        self.recurso = recurso
        self.result = result
        self.acessados = acessados
        self.dominio = dominio
    def desacumula(self):
        url = None
        self.rlock.acquire()
        ####regiao critica
        if len(self.recurso) > 0:
            url = self.recurso.pop()
        ##fim regiao critica
        self.rlock.release()

        if url != None:
            if url[len(url) - 1] == "/":
                url = url[0:len(url) - 1]
            print(f"A: {url}")
            self.acessados.append(url)
            ft = acessar_url(url)
            self.rlock.acquire()
            if ft != None:
                self.acessados.append(url)
                if (ft in self.result) == False:
                    if len(ft[1]) > 0:
                        self.result.append(ft)
                link_filtrados = filtrar_links(ft[2],self.dominio)
                for f in link_filtrados:
                    if f[len(f) - 1] == "/":
                        f = f[0:len(f) - 1]
                    podeEntrar = True
                    for lin in self.acessados:
                        if f == lin:
                            podeEntrar = False
                    for rec in self.recurso:
                        if rec == f:
                            podeEntrar = False

                    if ".zip" in f[len(f) - 5:len(f)] or ".pdf" in f[len(f) - 5:len(f)] or ".jpg" in f[len(f) - 5:len(f)] \
                            or ".c" in f[len(f) - 3:len(f)]  or ".ico" in f[len(f) - 5:len(f)] \
                            or ".doc" in f[len(f) - 5:len(f)] or ".rar" in f[len(f) - 5:len(f)] or \
                            ".png" in f[len(f) - 5:len(f)] or ".gif" in f[len(f) - 5:len(f)] or ".mp3" in f[len(f) - 5:len(f)] \
                            or ".txt" in f[len(f) - 5:len(f)] or ".mp4" in f[len(f) - 5:len(f)] or ".js" in f[len(f) - 4:len(f)]:
                        podeEntrar = False
                    if podeEntrar:
                        print(f"P: {f}")
                        self.recurso.append(f)
            self.rlock.release()
        ###fim da regiao critica
        #self.rlock.release()

    def run(self):
        print(f"Entrou - {self}")
        for i in range(5):
            self.rlock.acquire()
            self.desacumula()
            self.rlock.release()
        porcentagem = 100 - len(self.recurso) * 100 /(len(self.acessados) + len(self.recurso))
        porcentagem = round(porcentagem,2)
        print(f"{self} saiu\nFalta {len(self.recurso)} links\nCompletado: {porcentagem}%")

#
# if __name__ == "__main__":
#     recurso = []
#     result = []
#     acessados = []
#     url = "https://www.americanas.com.br"
#     recurso.append(url)
#     dominio = definirDominio(url)
#     rlock = RLock()
#     t = []
#     for i in range(1):
#         t.append(Desapegadora(rlock, recurso,result,dominio,acessados))
#         t[i].start()
#
#     for i in range(1):
#         t[i].join()
#
#     print("Resultado  final {}".format(recurso))
#     print(f"Resultado: {result}")