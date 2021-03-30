# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import ctypes
from webdriver_manager.chrome import ChromeDriverManager
import os
from pathlib import Path

from time import sleep
from bs4 import BeautifulSoup

from playsound import playsound

ctypes.windll.kernel32.SetConsoleTitleW("SATINDER")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def resource_path(relative):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = Path(sys._MEIPASS)
    else:
        bundle_dir = Path(__file__).parent
    return str(bundle_dir / relative)


now = datetime.now()

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options,)
driver.get("https://citas.sat.gob.mx/citasat/agregarcita.aspx")

while True:
    elem = None
    try:
        cls()
        print("Llene los campos necesarios en la pagina y NO cierre el navegador ni esta ventana.")
        print("Esperando calendario...")
        elem = WebDriverWait(driver, 240).until(expected_conditions.presence_of_element_located((By.ID, "Calendario")))
    except Exception as e:
        print(e)
        pass
    if elem:
        cls()
        print("Llene los campos necesarios en la pagina y NO cierre el navegador ni esta ventana.")
        print("Calendario encontrado.")
        print("Elija el mes en el que busca su cita y espere")
        soup = BeautifulSoup(driver.page_source.encode(encoding='utf-8').strip(), 'html.parser')
        html = soup.find("table", {"id": "Calendario"})
        while True:
            sleep(60)
            driver.execute_script("location.reload()")
            print("Actualizando calendario.")
            soup = BeautifulSoup(driver.page_source.encode(encoding='utf-8').strip(), 'html.parser')
            new_html = soup.find("table", {"id": "Calendario"})

            if html == new_html:
                dt_string = now.strftime("%H:%M:%S")
                print(f'{dt_string}:  Aun no hay citas. :(')
            else:
                print('Ya hay citas! :D')
                playsound(resource_path("alert.mp3"))
