import os
import glob
import shutil
import configparser

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

# caminho_origem = cfg['DEFAULT']['pasta_download']
if not os.path.exists(f"{os.getcwd()}\downloads"):
    os.makedirs(f"{os.getcwd()}\downloads")
    caminho_origem = f"{os.getcwd()}\downloads"

caminho_destino = os.getcwd() + '/RepositorioArquivosSimAm/'
class Arquivo:
    def renomear_arquivo(self, competencia,exercicio):
        os.chdir(caminho_origem)
        arquivos = (glob.glob('Layout_*'))
        self.criar_diretorio(exercicio)
        nome = {'Abertura de Exercício':'00','Janeiro':'01','Fevereiro':'02','Março':'03','Abril':'04','Maio':'05',
                'Junho':'06','Julho':'07','Agosto':'08','Setembro':'09','Outubro':'10','Novembro':'11',
                'Dezembro':'12','Encerramento de Exercício':'13'}
        os.rename(arquivos[0], caminho_destino + str(exercicio) + '/' + str(nome[competencia]) +'.zip')
        # os.rename(arquivos[0], caminho_destino + str(exercicio) + '/' + str(arquivos[0]) + '.zip')
    def criar_diretorio(self, exercicio):

        if os.path.exists(caminho_destino+str(exercicio)):
            return True
        else:
            caminho = os.makedirs(caminho_destino+str(exercicio))
            return False

    def listar_diretorios(self):
        pass

    def criar_arquivo_log(self):
        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)
        log = open(caminho_destino+'log.txt', 'w')
        log.close()

    def registrar_log(self, mensagem):
        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)
        os.chdir(caminho_destino)
        if os.path.exists("log.txt"):
            arquivo = open('log.txt', 'r')
            log = arquivo.readlines()
            log.append(mensagem+'\n')

            arquivo = open('log.txt', 'w')
            arquivo.writelines(log)

            arquivo.close()
            return True

        else:
            self.criar_arquivo_log()
            arquivo = open('log.txt', 'r')
            log = arquivo.readlines()
            log.append(mensagem + '\n')

            arquivo = open('log.txt', 'w')
            arquivo.writelines(log)
            arquivo.close()

    def contar_arquivos(self):
        exercicios_baixados = os.listdir(caminho_destino)
        exercicios_pendentes = []
        competencias_pendentes = []
        quantidade_exercicios = len(exercicios_baixados)
        print('\nQuantidade de Exercicios: '+str(quantidade_exercicios))
        self.registrar_log('\nQuantidade de Exercicios: '+str(quantidade_exercicios))
        print("Exercicios baixados: " + str(exercicios_baixados))
        self.registrar_log("Exercicios baixados: " + str(exercicios_baixados))

        for exercicio in exercicios_baixados:
            competecias_baixadas = os.listdir(caminho_destino + '\\' + str(exercicio))

            print("\nQuantidade Competencias baixadas por Exercicio: "+ str(len(competecias_baixadas))+" em "+ str(exercicio))
            self.registrar_log("\nQuantidade Competencias baixadas por Exercicio: "+ str(len(competecias_baixadas))+" em "+ str(exercicio))
            if len(competecias_baixadas) < 14:
                print("Exercicio com falta de Arquivos: " + str(exercicio))
                self.registrar_log("Exercicio com falta de Arquivos: " + str(exercicio))
                exercicios_pendentes.append(exercicio)
        return exercicios_pendentes

    def contar_competencias(self, exercicio):

        competencias = os.listdir(caminho_destino + '\\' + str(exercicio))
        return competencias

    def deletarZip(self):

        #Acesso a pasta onde estão os arquivos baixados
        os.chdir('C:\\Users\\equiplano\\Downloads\SimAm')
        #Listando os exercicios encontrados
        origem = os.listdir()
        for diretorios in origem:
            #acessando as pastas pelos exercicios encontrados
            os.chdir('C:\\Users\\equiplano\\Downloads\SimAm'+'\\'+diretorios)
            #Armazenando em lista arquivos com extensão .zip
            excluir = (glob.glob('*zip'))
            # Excluindo arquivos na pasta com extensão .zip
            for item in excluir:
                #Removendo item a item da lista
                os.remove(item)

    def grafico(self):
        grafico = []
        exercicios_baixados = os.listdir(caminho_destino)
        for exercicio in exercicios_baixados:
            competencias_baixadas = os.listdir(caminho_destino+'\\'+ exercicio)
            grafico.append([exercicio,competencias_baixadas])
        return grafico

    def validarArquivoTexto(self, exercicio, competencia):

        os.chdir(caminho_destino + '\\' + exercicio + '\\' + competencia + '\\Contabil')

        linhas = open('DiarioContabilidade.txt', 'r')
        texto = linhas.read()

        texto_competencia = texto.split('-')

        texto_exercicio = texto_competencia[0]
        texto_exercicio = texto_exercicio[-4::]

        entidade = texto.split('|')[0]
        print(entidade)

        return texto_exercicio, texto_competencia[1]

    def varrerDiretorios(self):
        dado = []
        dados = []
        exercicios = os.listdir(caminho_destino)

        for exercicio in exercicios:
            competencias = os.listdir(caminho_destino + exercicio)

            for competencia in competencias:
                pastas = os.listdir(caminho_destino + '\\' + exercicio + '\\' + competencia)
                for pasta in pastas:
                    arquivos = os.listdir(caminho_destino + exercicio + '\\' + competencia + '\\' + pasta)
                    dado = exercicio, competencia, arquivos, pasta
                    dados.append(dado)
        return dados

    def varrerDiretoriosFiltro(self, exercicio, competencia, pasta):
        dado = []
        dados = []
        arquivos = os.listdir(caminho_destino + str(exercicio) + '\\' + str(competencia) + '\\' + str(pasta))
        dado = arquivos
        dados.append(dado)
        return dados

        # print("Pastas diretorio principal exercícios: ", exercicios)
        # competencias = os.listdir(caminho_destino + '\\' + exercicios[0])
        # print("Competencias: ", competencias)
        # pastas = os.listdir(caminho_destino + '\\' + exercicios[0] + '\\' + competencias[1])
        # print("Pastas: ", pastas)
        # arquivos = os.listdir(caminho_destino + '\\' + exercicios[0] + '\\' + competencias[1] + '\\Contabil')
        # print("Arquivos txt: ", arquivos)
# exercicios = ['2016','2017']
# for exercicio in exercicios:
#     varredura = Arquivo.validarArquivoTexto(exercicio, '02')
#
#     print(varredura)
