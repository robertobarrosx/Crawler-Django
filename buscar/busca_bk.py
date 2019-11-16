from urllib.request import Request, urlopen
MAXTHREADS = 5
class Tag:
  def __init__(self, tag, quantidade):
    self.tag = tag
    self.quantidade = quantidade

  def __str__(self):
      return f"{self.tag} - {self.quantidade}"

def converter_link(url,continua):
    dominio = definirDominio_http(url)
    if "http" in continua:
        return continua
    if ".php" in url or ("?" in url and "=" in url):
        for i in range(len(url)-1,0,-1):
            if url[i] == "/":
                posicao = i
                break
        url = url[0:posicao]
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
        continua = continua[1:len(url) + 1]
    url_final = url +'/'+ continua

    if (dominio in url_final) == False:
        return "wsdbsadm"
    return url_final

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
    invalid = " >"
    otherinvalid = "()*&¨%<$#@}{[]+=_\'\"\/.,;:¹²³£¢¬ºª°?"

    for i, linha in enumerate(linhas):
        while "<" in linha:
            posicao = linha.find('<')
            tag = ""
            pode = True
            for percorrer in range(posicao+1,len(linha)):
                if linha[percorrer] in invalid:
                    break
                if "<!--" in linha:
                    if linha[percorrer] in otherinvalid:
                        break
                tag += linha[percorrer]
            for x in tag:
                if (x in validos) == False:
                    pode = False
                    break
            if (tag != "" and ("!" in tag) != True and ("/" in tag) != True) and pode or ("!doctype" in tag.lower() or "!--" in tag):
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
        podeAdicionar = True
        while "href=\"" in linha or "src=\"" in linha or "href=\'" in linha or "src=\'" in linha:
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
                if (linha[percorrer] == "\"" or linha[percorrer] == "\'"  or linha[percorrer] == "#" or linha[percorrer] == ")" or linha[percorrer] == " "):
                    break
                link += linha[percorrer]
            if ("http" in link or "mailto" in link or link == "" or ":" in link or ";" in link) == False :
                link = converter_link(url,link)
            # print(link)
            if ("http" in link or "mailto" in link )== False:
                continue
            # print("add")
            for esy in links:
                if esy.replace("/","") == link.replace("/",""):
                    podeAdicionar = False

            if link != "" and podeAdicionar:
                if link[len(link)-1] == "/":
                    link = link[0:len(link)-1]
                links.append(link)

        while "http:" in linha or "https:" in linha:
            posicao = linha.find('http')
            link = ""
            for percorrer in range(posicao,len(linha)):
                if(linha[percorrer] == "\"" or linha[percorrer] == "\'" or linha[percorrer] == "#" or linha[percorrer] == ")" or linha[percorrer] == " "):
                    break
                link += linha[percorrer]
            aux = link
            link = link.replace("\\","")
            for esy in links:
                if esy.replace("/","") == link.replace("/",""):
                    podeAdicionar = False
            if "http" in link == False or "://" in link == False or len(link) < 10:
                podeAdicionar = False
            if link != "" and podeAdicionar:
                if link[len(link)-1] == "/":
                    link = link[0:len(link)-1]
                links.append(link)
            linha = linha.replace(f"{aux}", "", 1)
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
    acessei = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    web_byte = urlopen(req).read()
    try:
        webpage = web_byte.decode('utf-8')
    except:
        webpage = web_byte.decode('latin-1')
    acessei.append(url)
    linhas = ler_linhas(webpage)
    todos_links = buscar_links(linhas,url)
    todas_tags = buscar_tags(linhas)
    return (url, todas_tags, todos_links)

def acessar(link):
    acessei = []
    url = link[0]
    if url[len(url) - 1] == "/":
        url = url[0:len(url) - 1]
    acessei.append(url)
    dominio = definirDominio(url)
    filtrado = filtrar_links(link[2], dominio)
    link_acessados =[]
    links_para_acessar = []
    link_acessados.append((url, link[1], link[2]))
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
            link_acessado = acessar_url(url)
            acessei.append(url)
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

#
#
# #
# search = ("http://www.gileduardo.com.br")
# #
# # print(link_acessados)
# link_acessados = acessar_url(search)
# print(link_acessados)
# eita = acessar(link_acessados)
# print(eita)