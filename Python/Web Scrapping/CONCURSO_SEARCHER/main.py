# Libraries
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from openpyxl import Workbook


table = {'Código':[], 'Tipo Oferta':[], 'Vínculo':[], 'Carreira':[], 'Categoria':[], 'Distrito':[], 'Organismo':[], 'Habilitações Literárias':[], 'Data Limite':[], 'Remuneração':[], 'Suplemento Mensal':[], 'Requisitos de Nacionalidade':[]}

#Define the path for chromedriver and defines the driver (base for all searchs)
path = os.path.dirname(os.path.abspath(__file__)) + '\chromedriver'
driver = webdriver.Chrome(path)
#Counter just to know in witch page we are currently
counter = 0
#Web page the program will open
page = 'https://www.bep.gov.pt/pages/oferta/Oferta_Pesquisa_basica.aspx'
driver.get(page)
#Important to have a sleep just in case the webpage take sometime to open
time.sleep(1)
#Search and click of the "Pesquisar" Button
driver.find_element(by=By.NAME, value="ctl00$ctl00$FormMasterContentPlaceHolder$ContentPlaceHolder1$ucSearch").click()
#Time in case the webpage takes sometime to search
time.sleep(1)

#Creation of the funtion that will
def extr_dados():

    time.sleep(1)
    main = driver.find_element(by=By.ID, value="ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_GvOfertaGestao")
    # pesquisa do body dentro do main
    body = main.find_element(by=By.TAG_NAME, value='tbody')
    # pesquisa do tr dentro do body
    tr = body.find_elements(by=By.TAG_NAME, value='tr')
    # para cada elemento dentro do TR vamos buscar os td, neste caso td é o nome de cada vada

    variavel = 0
    for linha in tr:

        variavel = variavel + 1
        variable = str(variavel)

        link = driver.find_element(by=By.LINK_TEXT, value=(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[1]').text))
        table['Código'].append(link.text)
        table['Tipo Oferta'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[2]').text)
        table['Vínculo'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[3]').text)
        table['Carreira'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[4]').text)
        table['Categoria'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[5]').text)
        table['Distrito'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[6]').text)
        table['Organismo'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[7]').text)
        table['Habilitações Literárias'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[8]').text)
        table['Data Limite'].append(driver.find_element_by_xpath(f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[9]').text)

        print(link.text) #Código da Oferta
        link.click()

        try:
            rem = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNORemuneracao').text
        except NoSuchElementException:
            rem = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblRemuneracao').text
        table['Remuneração'].append(rem)

        try:
            sm = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNOSupMensal').text
        except NoSuchElementException:
            sm = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblSuplemento').text
        table['Suplemento Mensal'].append(sm)

        try:
            tab = driver.find_element(by=By.LINK_TEXT, value="Requisitos de Admissão")
            tab.click()
        except NoSuchElementException:
            pass

        try:
            rn = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNOReqNac').text
        except NoSuchElementException:
            try:
                rn = driver.find_element_by_id('ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblRequisitosNacionalidade').text
            except NoSuchElementException:
                rn = 'Não Indicado'

        table['Requisitos de Nacionalidade'].append(rn)

        #time.sleep(1)

        driver.back()

try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, ">")))
    while driver.find_element(by=By.LINK_TEXT, value='>').text == '>':

        counter = counter + 1
        print(counter)
        extr_dados()

        driver.find_element(by=By.LINK_TEXT, value='>').click()

except NoSuchElementException:
    counter = counter + 1
    print(counter)
    extr_dados()

    tabela_completa = pd.DataFrame(table)

    tabela_completa.to_excel("output.xlsx")
    quit()
