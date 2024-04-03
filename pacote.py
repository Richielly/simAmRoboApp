import os
import shutil
from patoolib import extract_archive

# diretorio = "C:\\Users\\Equiplano\\PycharmProjects\\simAmRoboApp\\RepositorioArquivosSimAm\\"
diretorio = f"{os.getcwd()}/RepositorioArquivosSimAm/"

class Pacote:

    def descompactar(self,caminho_zip, diretorio_destino):

        # Verificar se a pasta existe
        if not os.path.exists(diretorio_destino):
            # Criar a pasta se não existir
            os.makedirs(diretorio_destino)
        elif os.listdir(diretorio_destino):
            # Pasta existe e não está vazia, então limpá-la
            for arquivo in os.listdir(diretorio_destino):
                caminho_arquivo = os.path.join(diretorio_destino, arquivo)
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
        # Descompactando o arquivo
        extract_archive(caminho_zip, outdir=diretorio_destino)

    def validar_arquivo(self, caminho_origem):
        diretorio_contabil = os.path.join(caminho_origem, 'Contabil')
        with open(os.path.join(diretorio_contabil, 'DiarioContabilidade.txt'), 'r') as linhas:
            texto = linhas.read()

        texto_competencia = texto.split('-')
        texto_exercicio = texto_competencia[0][-4:]

        return texto_exercicio, texto_competencia[1]

    def remover_pasta(self, diretorio):
        if os.path.exists(diretorio) and os.path.isdir(diretorio):
            shutil.rmtree(diretorio)

