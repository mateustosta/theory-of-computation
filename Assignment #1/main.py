import sys
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def url_handle():
    """Lê uma URL de STDIN e verifica se ela pertence
    ao domínio pt.wikipedia.org/wiki/
    """
    # regex para detectar se a url é válida/pertence ao domínio desejado
    URL_PATTERN = "((http|https)://)?(pt.wikipedia.org/wiki/)[a-zA-Z0-9%_]+"

    # lê de STDIN
    url = input("Digite a URL do artigo>").rstrip()

    # testa a url
    if re.match(URL_PATTERN, url):
        if "http" not in url or "https" not in url:
            return "https://"+url
        return url
    else:
        print(f"A URL informada não é válida ou não pertence ao domínio 'pt.wikipedia.org/wiki/'. URL informada: {url}")

        # chamada recursiva para ler uma nova url
        main()


def get_content_table(response, url):
    """Lê o HTML da página e exibe os tópicos do índice"""
    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # procura a tag
    content = response.findAll(attrs={"class": re.compile("toclevel-\d+\s?(tocsection-\d+)?")})

    # verifica se o artigo tem índice
    if content == []:
        print("Este artigo não tem índice.")
        print("\n\nPressione ENTER para voltar ao menu...")
        option = input("")
        menu(url)

    # template para o índice
    header = "-" * 40
    print("{header}\n{text:^40}\n{header}".format(header=header, text="Índice"))

    # printa o índice
    for ind in content:
        num = re.search(">\d+(\.\d+)*?<", str(ind))
        text = re.search("toctext\">[A-Za-z0-9À-ú\s\.\,\–\_\(\)\;\:\'\"]+", str(ind))

        if "." in num.group():
            occurrences = num.group().count(".")
            print("\t"*occurrences+"{0:>2s} {1}".format(num.group().replace(">", "").replace("<", "."), text.group().replace("toctext\">", "")))
        else:
            print("{0:>2s} {1}".format(num.group().replace(">", "").replace("<", "."), text.group().replace("toctext\">", "")))

    # volta ao menu
    print("\n\nPressione ENTER para voltar ao menu...")
    option = input("")
    menu(url)


def get_images(response, url):
    """Lê o HTML da página e exibe os nomes de arquivos de imagem"""
    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # procura a tag
    content = response.findAll(
        attrs={"href": re.compile("\/[a-zA-Z]+\/[a-zA-Z]+:.+\.[a-zA-Z]+")})

    # verifica se o artigo tem imagens
    if content == []:
        print("Este artigo não tem imagens.")
        print("\n\nPressione ENTER para voltar ao menu...")
        option = input("")
        menu(url)

    # template para as imagens
    header = "-" * 40
    print("{header}\n{text:^40}\n{header}".format(header=header, text="Imagens"))

    # array para excluir duplicados
    images = []
    i = 1
    for ind in content:
        text = re.search("\/[a-zA-Z]+\/[a-zA-Z]+:.+\.[a-zA-Z]+", str(ind))

        # tratamento para não printar repetidos
        if text.group() not in images:
            images.append(text.group())
            if ":" in os.path.basename(text.group()):
                print(f"{i}. {os.path.basename(text.group()).split(':')[1]}")
            else:
                print(f"{i}. {os.path.basename(text.group())}")
            i += 1

    # volta ao menu
    print("\n\nPressione ENTER para voltar ao menu...")
    option = input("")
    menu(url)


def get_references(response, url):
    """Lê o HTML da página e exibe as referências"""
    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # procura a tag
    content = response.findAll(attrs={"id": re.compile("^content$")})

    # template para as referências
    header = "-" * 40
    print("{header}\n{text:^40}\n{header}".format(header=header, text="Referências"))

    num = 1
    for ind in content:
        text = re.search('<h2><span .+ id="Referências">.+</h2>\n<ul>.+</li>\n?(<li>?.+</li>\n)+.+</ul>', str(ind))

        # caso em que as referências não são numeradas e não possuem links
        if text is not None:
            text = re.search("<ul>?(<li>.+</li>\n?)+</ul>", text.group())
            text = text.group().replace("<ul>", "").replace("<li>", "").replace("</ul>", "").replace("</li>", "")
            text = text.split("\n")

            for ref in text:
                print(f"{num}. {ref}")
                num += 1

    # volta ao menu
    print("\n\nPressione ENTER para voltar ao menu...")
    option = input("")
    menu(url)


def get_links(response, url):
    """Lê o HTML da página e exibe os links para outros
    artigos da wikipedia
    """
    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # procura a tag
    content = response.findAll(attrs={"id": re.compile("^content$")})

    # template para os links
    header = "-" * 40
    print("{header}\n{text:^40}\n{header}".format(
        header=header, text="Links para outros artigos"))

    i = 1
    # array para eliminar duplicados
    links = []
    for ind in content:
        text = re.findall("href=\"/wiki/[A-Za-z0-9À-ú\-\_\@\%\(\)\s]+\"", str(ind))

        for link in text:
            # tratamento para não printar repetidos
            if link.split('"')[1] not in links:
                links.append(link.split('"')[1])
                print("{0}. {1}".format(i, link.split('"')[1]))
                i += 1

    # volta ao menu
    print("\n\nPressione ENTER para voltar ao menu...")
    option = input("")
    menu(url)


def menu(url):
    """Exibe o menu em STDOUT"""
    # limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # menu em forma de tabela
    header = "-" * 120
    lines = [header, "{0:<25} {1}".format("Opção", "Descrição"), header,
             "{0:<25} {1}".format("1", "Listar os tópicos do índice do artigo"),
             "{0:<25} {1}".format("2", "Listar todos os nomes de arquivos de imagens presentes no artigo"),
             "{0:<25} {1}".format("3", "Listar todas as referências bibliográficas disponíveis na página"),
             "{0:<25} {1}".format("4", "Listar todos os links para outros artigos da Wikipédia que são citados no conteúdo do artigo"),
             "{0:<25} {1}".format("5", "Sair"), header]
    print("\n".join(lines))

    option = input("Digite uma opção>")

    # obtém o HTML da página
    try:
        html = urlopen(url)
    except HTTPError as error:
        print(error)
        sys.exit()
    except URLError as error:
        print(error)
        sys.exit()

    # lê o HTML
    response = BeautifulSoup(html.read(), "html5lib")

    if option == "1":
        get_content_table(response, url)
    elif option == "2":
        get_images(response, url)
    elif option == "3":
        get_references(response, url)
    elif option == "4":
        get_links(response, url)
    elif option == "5":
        sys.exit()
    else:
        # limpa a tela
        os.system("cls" if os.name == "nt" else "clear")
        print("Opção inválida!")
        time.sleep(1)
        menu(url)


def main():
    # lê e valida a URL
    url = url_handle()

    # invoca o menu
    menu(url)


if __name__ == "__main__":
    main()
