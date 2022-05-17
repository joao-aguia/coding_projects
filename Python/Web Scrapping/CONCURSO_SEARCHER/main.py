# Libraries
import sys
import os
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from openpyxl import Workbook

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# Counter just to know in witch page we are currently when the project is running
counter = 0
# Define the path for the excel file to be saved, in this case is the path of the project \Excel_Files
directory = r'%s' % application_path+'\Excel_Files'

# Define the name of the excel file, in this case will have the following format (Extraction_dd_mm_yy.xlsx) for today's date
file_name = ('Extraction_' + date.today().strftime("%d_%m_%y") + '.xlsx')

# Creation of the table with the headers of the excel file
table = {'Código': [], 'Tipo Oferta': [], 'Vínculo': [], 'Carreira': [], 'Categoria': [], 'Distrito': [],
         'Organismo': [], 'Habilitações Literárias': [], 'Descrição da Habilitação Literária': [], 'Data Limite': [],
         'Remuneração': [], 'Suplemento Mensal': [], 'Requisitos de Nacionalidade': []}

# Definion of the path for chromedriver and defines the driver (base for all searchs)
path = application_path + '\chromedriver'
driver = webdriver.Chrome(path)

# Website we're gonna analise and the delay of max time the program will wait to the website to open and see if the "Pesquisar" button is available
driver.get("https://www.bep.gov.pt/pages/oferta/Oferta_Pesquisa_basica.aspx")
delay = 3  # seconds

# The program will wait for the button to be available, after hes availailable the program will click it, if the page takes to long to load, the program go for "except"
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.NAME, 'ctl00$ctl00$FormMasterContentPlaceHolder$ContentPlaceHolder1$ucSearch')))
    driver.find_element(by=By.NAME,
                        value="ctl00$ctl00$FormMasterContentPlaceHolder$ContentPlaceHolder1$ucSearch").click()
except TimeoutException:
    print("Loading took too much time!")
    # Creation of the funtion that will assign every value to column defined on the table for excel
def extr_data():
    # time.sleep(1)

    # here we have a away to find what element we want by entering in each other tag_name so we know that TR is inside TBODY and TBODY is inside MAIN
    # we could have done this with "find_element_by_xpath" and have only one variable defined, but will leave it this way in case I need  to use this in other projects
    main = driver.find_element(by=By.ID,
                               value="ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_GvOfertaGestao")
    body = main.find_element(by=By.TAG_NAME, value='tbody')
    tr = body.find_elements(by=By.TAG_NAME, value='tr')
    var = 0

    for linha in tr:
        var = var + 1
        variable = str(var)

        link = driver.find_element(by=By.LINK_TEXT, value=(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[1]').text))
        table['Código'].append(link.text)

        table['Tipo Oferta'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[2]').text)
        table['Vínculo'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[3]').text)
        table['Carreira'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[4]').text)
        table['Categoria'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[5]').text)
        table['Distrito'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[6]').text)
        table['Organismo'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[7]').text)
        table['Habilitações Literárias'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[8]').text)
        table['Data Limite'].append(driver.find_element_by_xpath(
            f'/html/body/form[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[{variable}]/td[9]').text)

        #code of the offer
        print(link.text)
        link.click()

        try:
            rem = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNORemuneracao').text
        except NoSuchElementException:
            rem = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblRemuneracao').text
        table['Remuneração'].append(rem)

        try:
            sm = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNOSupMensal').text
        except NoSuchElementException:
            sm = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblSuplemento').text
        table['Suplemento Mensal'].append(sm)

        try:
            tab = driver.find_element(by=By.LINK_TEXT, value="Requisitos de Admissão")
            tab.click()
        except NoSuchElementException:
            pass

        try:
            dhl = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblDesHabLit').text
        except NoSuchElementException:
            try:
                dhl = driver.find_element_by_id(
                    'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblDescricaoHabilitacao').text
            except NoSuchElementException:
                dhl = 'Não Indicado'
        table['Descrição da Habilitação Literária'].append(dhl)

        try:
            rn = driver.find_element_by_id(
                'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblNOReqNac').text
        except NoSuchElementException:
            try:
                rn = driver.find_element_by_id(
                    'ctl00_ctl00_FormMasterContentPlaceHolder_ContentPlaceHolder1_lblRequisitosNacionalidade').text
            except NoSuchElementException:
                rn = 'Não Indicado'
        table['Requisitos de Nacionalidade'].append(rn)

        # time.sleep(1)
        driver.back()


try:
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, ">")))
    while driver.find_element(by=By.LINK_TEXT, value='>').text == '>':
        counter = counter + 1
        print(counter)
        extr_data()

        driver.find_element(by=By.LINK_TEXT, value='>').click()

except NoSuchElementException:
    counter = counter + 1
    print(counter)
    extr_data()

    tabela_completa = pd.DataFrame(table)
    tabela_completa.to_excel(os.path.join(directory, file_name))
driver.close()
sys.exit()

