# -*- coding:utf-8 -*-
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By # Usando o novo formato de localização de elementos
from datetime import datetime
import time
import os
# from pacote import Pacote
from arquivo import Arquivo
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

options = Options()
options.add_experimental_option("prefs", {"download.default_directory": f"{os.getcwd()}\downloads"})
print(f"{os.getcwd()}\downloads")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

arq = Arquivo()
class Consulta:
    def loginSimAm(self, usuario, senha):
        try:
            global browser
            browser.get("https://servicos.tce.pr.gov.br/tcepr/municipal/simam/Paginas/Consulta.aspx")

            # username = browser.find_element_by_id("Login")
            # password = browser.find_element_by_id("Senha")
            # Usando o novo formato de localização de elementos
            username = browser.find_element(By.ID, "Login")
            password = browser.find_element(By.ID, "Senha")

            username.send_keys(usuario)
            password.send_keys(senha)
            time.sleep(5)
            # login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
            login_attempt = browser.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            arq.registrar_log(" ########## Acesso realizado com sucesso em: " + datetime.now().strftime("%d/%m/%Y %H:%M" + " ##########"))
            return True
        except Exception as e:
            # Registrar o erro completo no log
            error_message = f"Problema ao tentar fazer acesso em: {datetime.now().strftime('%d/%m/%Y %H:%M')}. Erro: {str(e)}"
            arq.registrar_log(error_message)
            # Exibir o erro no console para depuração
            print(error_message)

        return False

    def rota(self, exercicio, competencia):

        try:
            global browser
            browser.find_element(By.XPATH,"//select[@name='ctl00$ContentPlaceHolder1$ddlTipo']/option[text()='Movimento Mês']").click()
            time.sleep(2)
            browser.find_element(By.XPATH,"//select[@name='ctl00$ContentPlaceHolder1$ddlAno']/option[text()="+str(exercicio)+"]").click()
            time.sleep(1)
            browser.find_element(By.XPATH,"//select[@name='ctl00$ContentPlaceHolder1$ddlMes']/option[text()='"+competencia+"']").click()
            time.sleep(1)

            checkboxes = browser.find_elements(By.XPATH, "//*[@type='checkbox']")

            for marcar in checkboxes:
                marcar.click()
                time.sleep(3)
            time.sleep(3)
            self.processar(exercicio, competencia)

            return True


        except Exception as e:

            # Capturando o erro e registrando no log
            error_message = f"Problema ao tentar selecionar arquivos: {datetime.now().strftime('%d/%m/%Y %H:%M')}. Erro: {str(e)}"
            arq.registrar_log(error_message)
            print(error_message)  # Exibir o erro no console para facilitar a depuração

        return False

    def processar(self, exercicio, competencia):
        try:
            global browser
            browser.find_element(By.ID, 'ContentPlaceHolder1_btnProcessar').click()
            # Registrando o log e exibindo a mensagem no console
            log_message = f"Processamento em andamento ({competencia}/{str(exercicio)}) iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            arq.registrar_log(log_message)
            print(log_message)
            # Chamando a função de download
            self.download(exercicio, competencia)
            return True
        except Exception as e:
            # Capturando e registrando o erro
            error_message = f"Erro ao processar arquivos para {competencia}/{str(exercicio)}: {str(e)}"
            arq.registrar_log(error_message)
            print(error_message)  # Exibindo o erro no console para facilitar a depuração

            return False

    def liberarDownload(self, exercicio, competencia):
        global browser
        time.sleep(7)  # Aguarda antes de tentar novamente

        try:
            # Atualizando a página
            browser.find_element(By.ID, 'ContentPlaceHolder1_btnAtualizarPagina').click()

            # Tentando encontrar e clicar no botão de download
            download_button = browser.find_element(By.ID, 'ContentPlaceHolder1_btnDownload')
            download_button.click()
            time.sleep(3)

            # Renomeando o arquivo após o download
            arq.renomear_arquivo(competencia, exercicio)
            # Pacote.decompactarCmd()
            # time.sleep(5)
            # Arquivo.deletarZip()

            return False  # Download realizado com sucesso, não precisa tentar novamente
        except Exception as e:
            # Caso o botão de download ainda não esteja disponível ou algum erro ocorra
            error_message = f"Erro ao tentar liberar download para {competencia}/{str(exercicio)}: {str(e)}"
            arq.registrar_log(error_message)
            print(error_message)  # Exibir o erro no console para facilitar a depuração

            return True  # Retorna True para continuar tentando, já que o botão ainda não apareceu

    def download(self, exercicio, competencia):
        try:
            # Enquanto a função liberarDownload retorna True, continuar tentando
            while self.liberarDownload(exercicio, competencia):
                time.sleep(6)

            # Registro no log após o início do download
            log_message = f"Download ({competencia}/{str(exercicio)}) iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            arq.registrar_log(log_message)
            print(log_message)

        except Exception as e:
            # Captura de qualquer exceção e registro do erro
            error_message = f"Erro ao iniciar o download para {competencia}/{str(exercicio)}: {str(e)}"
            arq.registrar_log(error_message)
            print(error_message)  # Exibir o erro no console para facilitar a depuração

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
                self.rota(exercicio, competencia)

        arq.registrar_log(" ########## Processo finalizado em: " + datetime.now().strftime('%d/%m/%Y %H:%M' + " ##########"))
        self.finalizarNavegador()
