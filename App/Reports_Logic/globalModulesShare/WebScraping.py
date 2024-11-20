# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from urllib3.exceptions import InsecureRequestWarning

# import os
from .ContenedorVariables import Variables
from .mensajes_alertas import Mensajes_Alertas



class Web_scraping:
    def __init__(self):
        self.fecha_inicial_df_merge = Variables().date_movement_config_document().replace(day=1)
        self.fecha_final_df_merge = Variables().date_movement_config_document()
    def obtener_dolares(self, fecha_inicial, fecha_final):
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.ruta_dof = f'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={self.fecha_inicial}&hfecha={self.fecha_final}#gsc.tab=0'
        # Silenciar la advertencia de SSL
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Realizar la solicitud con SSL deshabilitado
        response = requests.get(self.ruta_dof, verify=False)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
            div = self.soup.find('div', {'id':'cuerpo_principal'})
            if div:
                self.tabla = div.find('table', {'class':'Tabla_borde'})
                if self.tabla:
                    tabla_html = str(self.tabla)
                    df = pd.read_html(StringIO(tabla_html))[0]
                    df.columns = df.iloc[0]
                    df.drop(index=0, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    if 'Fecha' in df.columns:
                        df["Fecha"] = pd.to_datetime(df['Fecha'], dayfirst=True)
                        
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
                        return juntar_dos
                else:
                    return None
            else:
                return None
        else:
            return None

# Web_scraping().obtener_dolares('01/11/2024','20/11/2024')
# Web_scraping()
