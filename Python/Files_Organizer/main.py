from PIL import Image # Library Pillow para a obtenção da data em que a foto foi tirada
import os # Lybrary Miscellaneous para a criação da pasta
import hashlib # Library para a criação de HASH de um ficheiro
import calendar # Library para a conversão de numero em mês
import shutil # Library para copiar ficheiros
path_origem = r"C:\Users\joao_\Desktop\Projeto Python\Origem"
path_destino = r"C:\Users\joao_\Desktop\Projeto Python\Destino"
txt_duplicados = os.path.join(path_destino,"Duplicados","Duplicados.txt") # diretoria e nome do txt de duplicados
lista = []

# Gera a diretoria, o ficheiro do path_origem
for root, dirs, files in os.walk(path_origem):
    for name in files:
        path_origem_ficheiro = (os.path.join(root, name)) #junta a diretoria do ficheiro mais o nome do ficheiro
        nome_ficheiro = (name) #mostra somente o nome do ficheiro
        #lista
        #ficheiro.append(os.path.join(root, name)) #junta diretoria com nome ficheiro

# Criação do codigo HASH
        def hash_file(path_origem_ficheiro):
            h = hashlib.sha1()  # Criação de um ficheiro HASH
            with open(path_origem_ficheiro, 'rb') as file:  # Abre o ficheiro em reading em modo binario
                chunk = 0  # loop até ao final do ficheiro
                while chunk != b'':
                    chunk = file.read(1024)  # Lê somente 1024 bytes de cada vez
                    h.update(chunk)
            return h.hexdigest()

        hash = (hash_file(path_origem_ficheiro))
        #print(root, name, hash)

# Validação se existe o hash na lista, caso exista cria a pasta duplicados e copia a imagem para dentro dessa pasta
        if hash in lista:
            dir = os.path.join(path_destino, "Duplicados")
            if not os.path.exists(dir):
                os.mkdir(dir)
            shutil.copyfile(path_origem_ficheiro, os.path.join(dir, nome_ficheiro))
# Criação do ficheiro txt de duplicados que indica qual o ficheiro duplicado e em qual diretoria ele estava a tentar ser inserido
            txt = open(txt_duplicados,
                       "a+")  # a+ cria um novo ficheiro e vai fazendo append das linhas umas em baixo das outras
            txt.write(
                f'{nome_ficheiro} -----> {os.path.join(path_destino, data[0:4], calendar.month_name[int(data[5:7])], data[8:10])}\n')
        else:
#Criação das pastas com a data que a foto foi tirada
            data = Image.open(path_origem_ficheiro)._getexif()[36867] #Obtem a data e hora que foto foi tirada
# Cria a pasta do Ano
            dir = os.path.join(path_destino,data[0:4])
            if not os.path.exists(dir):
                os.mkdir(dir)
# Cria a pasta do mês dentro do ano
            dir = os.path.join(path_destino, data[0:4], calendar.month_name[int(data[5:7])])
            if not os.path.exists(dir):
                os.mkdir(dir)
# Cria a pasta do dia dentro do mês e Ano
            dir = os.path.join(path_destino, data[0:4], calendar.month_name[int(data[5:7])], data[8:10])
            if not os.path.exists(dir):
                os.mkdir(dir)

# Copia a imagem de uma diretoria para outra
            shutil.copyfile(path_origem_ficheiro, os.path.join(dir, nome_ficheiro))
        # Inserção na Lista
            lista.append((hash_file(path_origem_ficheiro))) #junta diretoria com nome ficheiro