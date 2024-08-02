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
        
        base_path = os.path.dirname(os.path.abspath(__file__))

        self.chromedriver_path = os.path.join(base_path, '..', '..', 'chromedriver', 'chromedriver.exe')

        # Normalizar la ruta para evitar problemas con diferentes sistemas operativos
        self.chromedriver_path = os.path.normpath(self.chromedriver_path)
        print(self.chromedriver_path)

        # driver = webdriver.Chrome(executable_path=chromedriver_path)


        self.fecha_inicial_df_merge = Variables().date_movement_config_document().replace(day=1)
        self.fecha_final_df_merge = Variables().date_movement_config_document()


    def obtener_dolares(self, fecha_inicial, fecha_final):
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.ruta_dof = f'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={self.fecha_inicial}&hfecha={self.fecha_final}#gsc.tab=0'
        print("Ruta del dof: ", self.ruta_dof)
        # Configuración del navegador
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecuta el navegador en modo headless

        # Reemplaza con la ruta a tu chromedriver
        service = Service(self.chromedriver_path)  
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
            df.columns = df.iloc[0]
            df.drop(index=0, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df["Fecha"] = pd.to_datetime(df['Fecha'],dayfirst=True)
            # RANGO COMPLETO DE FECHAS

            rango_completo_fechas = pd.date_range(start=self.fecha_inicial_df_merge, end=self.fecha_final_df_merge, freq='D')

            df_completo_fechas = pd.DataFrame(rango_completo_fechas, columns=['Fecha'])
            juntar_dos = pd.merge(df_completo_fechas, df, on='Fecha', how='left')
            # Rellenar los NaN con el valor anterior
            juntar_dos['Valor'] = juntar_dos['Valor'].fillna(method='ffill')
            for column_name in juntar_dos.columns:
                if "fecha" in column_name.lower():
                    juntar_dos = Variables().global_date_format_america(juntar_dos, column_name)
                    juntar_dos = Variables().global_date_format_dmy_mexican(juntar_dos, column_name)
                else:
                    pass
            juntar_dos['Valor'] = pd.to_numeric(juntar_dos['Valor'])
            driver.quit()
            return juntar_dos
        else:
            return None
# Web_scraping().obtener_dolares('01/07/2024','31/07/2024')
# Web_scraping()
