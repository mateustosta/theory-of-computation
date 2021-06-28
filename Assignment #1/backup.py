import sys
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Função para verificar se a URL informada é válida


def check_URL(url):
    URL_PATTERN = ("((http|https)://)(pt.wikipedia.org/wiki/)[a-zA-Z0-9%_]+")

    if len(url) == 1 or len(url) > 2:
        print("Modo de uso: python main.py URL")
        print("Ex: python main.py https://pt.wikipedia.org/wiki/Simula%C3%A7%C3%A3o_de_reservat%C3%B3rio")
        sys.exit()
    else:
        if re.match(URL_PATTERN, url[1]):
            return url[1]
        else:
            print(
                "A URL informada não é válida ou não pertence ao domínio: pt.wikipedia.org/wiki/")
            sys.exit()

# Função para lidar com o menu


def menu(url):
    # Limpa a tela
    os.system('cls' if os.name == 'nt' else 'clear')

    # Menu em forma de tabela
    header = "-" * 120
    lines = [header, "{0:<25s} {1}".format('Opção', 'Descrição'), header,
             "{0:<25s} {1}".format('1', 'Listar os tópicos do índice do artigo'), "{0:<25s} {1}".format(
                 '2', 'Listar todos os nomes de arquivos de imagens presentes no artigo'),
             "{0:<25s} {1}".format('3', 'Listar todas as referências bibliográficas disponíveis na página'), "{0:<25s} {1}".format(
        '4', 'Listar todos os links para outros artigos da Wikipédia que são citados no conteúdo do artigo'),
        "{0:<25s} {1}".format('5', 'Sair'), header]
    print("\n".join(lines))

    op = input("Digite uma opção: ")

    # Pega o HTML da página
    try:
        html = urlopen(url)
    except HTTPError as error:
        print(error)
        sys.exit()
    except URLError:
        print("Erro no servidor.")
        sys.exit()

    # Lê o html
    res = BeautifulSoup(html.read(), "html5lib")

    # Listar tópicos do índice
    if op == '1':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(
            attrs={'class': re.compile('toclevel-\d+\s?(tocsection-\d+)?')})

        # Verifica se o artigo tem índice
        if content == []:
            print("Este artigo não tem índice.")
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

        # Printa o índice
        header = "-" * 40
        print(header + "\n{0:^40s}".format("Índice") + '\n' + header)
        for ind in content:
            num = re.search('>\d+(\.\d+)*?<', str(ind))
            text = re.search(
                'toctext\">[A-Za-z0-9À-ú\s\.\,\–\_\(\)\;\:\'\"]+', str(ind))

            if '.' in num.group():
                occ = num.group().count('.')
                print("\t" * occ + "{0:>2s} {1}".format(num.group().replace(
                    '>', '').replace('<', '.'), text.group().replace('toctext">', '')))
            else:
                print("{0:>2s} {1}".format(num.group().replace('>', '').replace(
                    '<', '.'), text.group().replace('toctext">', '')))

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

    elif op == '2':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(attrs={'href': re.compile(
            '\/[a-zA-Z]+\/[a-zA-Z]+:.+\.[a-zA-Z]+')})

        # Verifica se o artigo tem imagens
        if content == []:
            print("Este artigo não tem imagens.")
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

        # Printa as imagens
        header = "-" * 40
        print(header + "\n{0:^40s}".format("Imagens") + '\n' + header)
        images = []
        i = 1
        for ind in content:
            text = re.search('\/[a-zA-Z]+\/[a-zA-Z]+:.+\.[a-zA-Z]+', str(ind))

            # Tratamento para não printar repetidos
            if text.group() not in images:
                images.append(text.group())
                if ':' in os.path.basename(text.group()):
                    print("{}. ".format(i) +
                          os.path.basename(text.group()).split(':')[1])
                else:
                    print("{}. ".format(i) + os.path.basename(text.group()))
                i += 1

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

    elif op == '3':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag (neste caso a tag MAIN onde o artigo em si fica)
        content = res.findAll(attrs={'id': re.compile('^content$')})

        # Verifica se o artigo tem referências
        if content == []:
            print("Este artigo não tem referências.")
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

        # Printa as referências
        header = "-" * 40
        print(header + "\n{0:^40s}".format("Referências") + '\n' + header)
        num = 1  # índice das referências
        for ind in content:
            text = re.search(
                '<h2><span .+ id="Referências">.+</h2>\n<ul>.+</li>\n?(<li>?.+</li>\n)+.+</ul>', str(ind))
            # caso onde as referências não são numeradas e não possuem links
            if text is not None:
                text = re.search('<ul>?(<li>.+</li>\n?)+</ul>', text.group())
                text = text.group().replace('<ul>', '').replace(
                    '<li>', '').replace('</ul>', '').replace('</li>', '')
                text = text.split('\n')
                for ref in text:
                    print("{}. ".format(num) + ref)
                    num += 1
            # caso onde as referências são numeradas e possuem (ou não) links
            else:
                text = re.search(
                    '<ol class=\"references\">[\s\S]*</ol>', str(ind))
                text = text.group().split('\n')
                for ref in text:
                    tmp = re.search(
                        '<cite class=\"citation book\">(.*)<i>', ref)
                    if tmp is not None:
                        tmp = re.search('>(.*)<', tmp.group())
                        print("{}. {}".format(
                            num, tmp.group().replace('<', '').replace('>', '')))
                        num += 1
                    else:
                        tmp = re.search(
                            '<span class=\"reference-text\">(.*)</span>', ref)
                        if tmp is not None:
                            tmp = re.search('>(.*)<', tmp.group())
                            print('{}. {}'.format(
                                num, tmp.group().replace('<', '').replace('>', '')))
                            num += 1

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

    elif op == '4':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag (neste caso a tag MAIN onde o artigo em si fica)
        content = res.findAll(attrs={'id': re.compile('^content$')})

        # Verifica se o artigo tem links
        if content == []:
            print("Este artigo não tem links para outros artigos.")
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

        # Printa os links
        header = "-" * 40
        print(
            header + "\n{0:^40s}".format("Links para outros artigos") + '\n' + header)
        i = 1
        links = []
        for ind in content:
            text = re.findall(
                'href=\"/wiki/[A-Za-z0-9À-ú\-\_\@\%\(\)\s]+\"', str(content))

            for link in text:
                # Tratamento para não printar repetidos
                if link.split("\"")[1] not in links:
                    links.append(link.split("\"")[1])
                    print("{}. ".format(i) + link.split("\"")[1])
                    i += 1

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)
    elif op == '5':
        sys.exit()
    else:
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Opção inválida!")
        time.sleep(2)  # aguarda 2 segundos
        menu(url)  # invoca a função menu() recursivamente


if __name__ == "__main__":
    # Verifica se a URL informada é válida
    url = check_URL(sys.argv)

    # Menu
    menu(url)
