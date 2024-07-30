from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os
import sys
from .ContenedorVariables import Variables

class Web_scraping:
    def __init__(self):
        self.fecha_inicial = ''
        self.fecha_final = ''
        self.fin_ruta = r"/Reports_Logic/"
        if getattr(sys, 'frozen', False):
            # Ruta en el entorno empaquetado
            self.driver_folder = os.path.join(sys._MEIPASS, 'chromedriver')
            self.split_path = self.driver_folder.replace('\\','/').split(self.fin_ruta )[0]
        else:
            # Ruta en desarrollo
            self.driver_folder = os.path.join(os.path.dirname(__file__), 'chromedriver')
            self.split_path = self.driver_folder.replace('\\','/').split(self.fin_ruta )[0]
        self.chrome_driver_path = os.path.join(self.split_path,'chromedriver', 'chromedriver.exe')
        print("Ruta del chromedriver: ", self.chrome_driver_path)

    def obtener_dolares(self, fecha_inicial, fecha_final):
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.ruta_dof = f'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={self.fecha_inicial}&hfecha={self.fecha_final}#gsc.tab=0'
        print("Ruta del dof: ", self.ruta_dof)
        # Configuración del navegador
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecuta el navegador en modo headless

        # Reemplaza con la ruta a tu chromedriver
        service = Service(self.chrome_driver_path)  
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Abrir la página
        driver.get(self.ruta_dof)

        # Espera opcional para asegurarse de que la página se ha cargado completamente
        driver.implicitly_wait(30)  # Espera hasta 10 segundos

        # Encontrar el div que contiene la tabla
        div = driver.find_element(By.ID, 'cuerpo_principal')

        # Obtener el HTML del div
        html = div.get_attribute('outerHTML')

        # Usar BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar la tabla con la clase 'tabla_borde'
        table = soup.find('table', {'class': 'Tabla_borde'})

        # Verificar si se encontró la tabla
        if table:
            # Convertir la tabla a un DataFrame
            table_html = str(table)
            df = pd.read_html(StringIO(table_html))[0]

            driver.quit()
            return df
        else:
            return None
