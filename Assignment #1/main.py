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
                "{0:<25s} {1}".format('3', 'Listar todas as referências bibliográficas disponíveis na página'), "{0:<25s} {1}".format('4', 'Listar todos os links para outros artigos da Wikipédia que são citados no conteúdo do artigo'),
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
    res = BeautifulSoup(html.read(),"html5lib");

    # Listar tópicos do índice
    if op == '1':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(attrs = { 'class' : re.compile('toclevel-\d+ tocsection-\d+') })

        # Verifica se o artigo tem índice
        if content == []:
            print("Este artigo não tem índice.")
            time.sleep(3)
            sys.exit()

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

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

    elif op == '2':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(attrs = { 'href' : re.compile('\/[a-zA-Z]+\/[a-zA-Z]+:[a-zA-Z0-9\_\-\,]+\.[a-zA-Z]+') })

        # Verifica se o artigo tem imagens
        if content == []:
            print("Este artigo não tem imagens.")
            time.sleep(3)
            sys.exit()

        # Printa as imagens
        header = "-" * 40
        print(header +  "\n{0:^40s}".format("Imagens") + '\n' + header)
        images = []
        for ind in content:
            text = re.search('\/[a-zA-Z]+\/[a-zA-Z]+:[a-zA-Z0-9\_\-\,]+\.[a-zA-Z]+', str(ind))
            
            # Tratamento para não printar repetidos
            if text.group() not in images:
                images.append(text.group())
                if ':' in os.path.basename(text.group()):
                    print(os.path.basename(text.group()).split(':')[1])
                else:
                    print(os.path.basename(text.group()))

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)

    elif op == '3':
        # Limpa a tela
        os.system('cls' if os.name == 'nt' else 'clear')

        # Procura a tag
        content = res.findAll(attrs = { 'id' : re.compile('cite_note-\d+') })

        # Verifica se o artigo tem referências
        if content == []:
            print("Este artigo não tem referências.")
            time.sleep(3)
            sys.exit()  

        # Printa as referências
        header = "-" * 40
        print(header +  "\n{0:^40s}".format("Imagens") + '\n' + header)
        num = 1  #  índice das referências
        for ind in content:
            text = re.search('<span class="reference-text"><.+>?[a-zA-Z0-9À-ú]+>', str(ind))
            print(str(num) + ' ' + text.group()) #TODO: Parei aqui
            num+=1

        # Volta ao menu
        while True:
            print("\n\nPressione ENTER para voltar ao menu...")
            op = input("")
            menu(url)    

    elif op == '4':
        pass
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
