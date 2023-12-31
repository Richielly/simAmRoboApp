# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import time
from pacote import Pacote
from arquivo import Arquivo

import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

browser = webdriver.Chrome(ChromeDriverManager().install())
arq = Arquivo()
class Consulta:
    def loginSimAm(self, usuario,senha):
        try:
            browser.get("https://servicos.tce.pr.gov.br/tcepr/municipal/simam/Paginas/Consulta.aspx")
            username = browser.find_element_by_id("Login")
            password = browser.find_element_by_id("Senha")
            username.send_keys(usuario)
            password.send_keys(senha)
            time.sleep(5)
            login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
            login_attempt.submit()
            arq.registrar_log(" ########## Acesso realizado com sucesso em: " + datetime.now().strftime('%d/%m/%Y %H:%M' +" ##########"))
            return True
        except: arq.registrar_log("Problema ao tentar fazer acesso em: " + datetime.now().strftime('%d/%m/%Y %H:%M'))
        return False
#browser.find_element_by_id('ContentPlaceHolder1_btnFechar').click()

    def rota(self, exercicio, competencia):

        try:
            global browser
            browser.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$ddlTipo']/option[text()='Movimento Mês']").click()
            time.sleep(2)
            browser.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$ddlAno']/option[text()="+str(exercicio)+"]").click()
            time.sleep(1)
            browser.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$ddlMes']/option[text()='"+competencia+"']").click()
            time.sleep(1)

            checkboxes = browser.find_elements_by_xpath("//*[@type='checkbox']")

            for marcar in checkboxes:
                marcar.click()
                time.sleep(3)
            time.sleep(3)
            #Arquivo.registrar_log()
            # texto = browser.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$hfLayout']/value[text()]")
            # print(texto)
            self.processar(exercicio,competencia)

            return True

        except: arq.registrar_log("Problema ao tentar selecionar arquivos: " + datetime.now().strftime('%d/%m/%Y %H:%M'))

    def processar(self, exercicio, competencia):
        try:
            global browser
            browser.find_element_by_id('ContentPlaceHolder1_btnProcessar').click()
            arq.registrar_log("Processamento em andamento (" +competencia+"/"+str(exercicio)+ ")iniciado em: " + datetime.now().strftime('%d/%m/%Y %H:%M'))
            print("Processamento em andamento (" +competencia+"/"+str(exercicio)+ ")iniciado em: " + datetime.now().strftime('%d/%m/%Y %H:%M'))
            self.download(exercicio, competencia)

            return True
        except: return False

    def liberarDownload(self, exercicio, competencia):
        global browser
        time.sleep(7)
        browser.find_element_by_id('ContentPlaceHolder1_btnAtualizarPagina').click()
        try:
            browser.find_element_by_id('ContentPlaceHolder1_btnDownload').click()
            time.sleep(3)
            arq.renomear_arquivo(competencia, exercicio)
            # Pacote.decompactarCmd()
            # time.sleep(5)
            # Arquivo.deletarZip()
        except: return True
        return False

    def download(self, exercicio, competencia):
        while(self.liberarDownload(exercicio, competencia)):
            time.sleep(6)
        arq.registrar_log("Download (" +competencia+"/"+str(exercicio)+ ") iniciado em: "+datetime.now().strftime('%d/%m/%Y %H:%M'))
        print("Download (" +competencia+"/"+str(exercicio)+ ") iniciado em: "+datetime.now().strftime('%d/%m/%Y %H:%M'))

    def finalizarNavegador(self):
        global browser
        print("Navegador finalizado em: "+datetime.now().strftime('%d/%m/%Y %H:%M'))
        browser.close()
        arq.registrar_log("Navegador finalizado em: "+datetime.now().strftime('%d/%m/%Y %H:%M'))

    def start(self, exercicios, competencias, usuario, senha):

        logado = self.loginSimAm(usuario, senha)
        time.sleep(7)

        for exercicio in exercicios:
            for competencia in competencias:
                self.rota(exercicio,competencia)

        arq.registrar_log(" ########## Processo finalizado em: " + datetime.now().strftime('%d/%m/%Y %H:%M' + " ##########"))
        self.finalizarNavegador()


