# -*- coding:utf-8 -*-
from zipfile import ZipFile
from pyunpack import Archive
import os
import sys
import time
import shutil
from arquivo import Arquivo as arq


        #Extrair todos os arquivos mas sem as devidas pastas arquivo final txt
            #os.system('7z e 00.zip -oC:\\caminho de destino')
        #Extrair todos os arquivos conforme sua estrutura de pastas
            #os.system('7z x '+str(nome[competencia])+'.zip -oC:\\caminho de destino)

diretorio = "C:\\Users\\equiplano\\Downloads\SimAm\\"

class Pacote:

    def descompactar(self, exercicio, competencia):

        if os.path.exists("C:\\Users\\equiplano\\Downloads\\SimAm\\"+str(exercicio)+'\\'+str(competencia)):
            Archive(diretorio + str(exercicio) + '\\' + str(competencia + '.zip')).extractall(diretorio + str(exercicio) + '\\' + str(competencia)+'\\')
        else:
            caminho = os.makedirs("C:\\Users\\equiplano\\Downloads\\SimAm\\"+str(exercicio)+'\\'+str(competencia))
            Archive(diretorio + str(exercicio) + '\\' + str(competencia + '.zip')).extractall(diretorio + str(exercicio) + '\\' + str(competencia)+'\\')
