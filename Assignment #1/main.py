import sys,re,os,time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Função para verificar se a URL informada é válida
def check_URL(url):
    URL_PATTERN = ("((http|https)://)(pt.wikipedia.org/wiki/)[a-zA-Z0-9%_]+")

    if len(url) == 1 or len(url) > 2:
        sys.exit()
    else:
        if re.match(URL_PATTERN, url[1]):
            return url[1]
        else:
            sys.exit()

# Função para lidar com o menu
def menu(url):
    # Limpa a tela
    os.system('cls' if os.name == 'nt' else 'clear')

    # Menu em forma de tabela
    header = "-" * 120
    lines = [header, "{0:<25s} {1}".format('Opção', 'Descrição'), header,
                "{0:<25s} {1}".format('1', 'Listar os tópicos do índice do artigo'), "{0:<25s} {1}".format('2', 'Listar todos os nomes de arquivos de imagens presentes no artigo'),
                "{0:<25s} {1}".format('3', 'Listar todas as referências bibliográficas disponíveis na página'), "{0:<25s} {1}".format('4', 'Listar todos os links para outrosartigos da Wikipédia que são citados no conteúdo do artigo'), header]
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
    
    # Lê o html e procura pela tag MAIN
    res = BeautifulSoup(html.read(),"html5lib");

    # Listar tópicos do índice
    if op == '1':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(attrs = { 'class' : re.compile('toclevel-\d+ tocsection-\d+') })

        # Printa o índice
        header = "-" * 40
        print(header +  "\n{0:^40s}".format("Índice") + '\n' + header)
        for ind in content:
            num = re.search('>\d+(\.\d+)*?<', str(ind))
            text = re.search('toctext\">[A-Za-z0-9À-ú\s]+', str(ind))
            if '.' in num.group():
                occ = num.group().count('.')
                print("\t" * occ + "{0:>2s} {1}".format(num.group().replace('>', '').replace('<', '.'), text.group().replace('toctext">', '')))
            else:  
                print("{0:>2s} {1}".format(num.group().replace('>', '').replace('<', '.'), text.group().replace('toctext">', '')))
    elif op == '2':
        pass
    elif op == '3':
        pass
    elif op == '4':
        pass
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
