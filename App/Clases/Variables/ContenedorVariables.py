#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
from datetime import *
from webbrowser import *
import calendar
import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class Variables():
    def __init__(self):
        self.separador = os.sep
        self.carpeta_documentos_trabajos_sonora = 'SDR_Documentos_Kenworth_Sonora'
        self.carpeta_documentos_trabajos_kweste = 'SDR_Documentos_Kenworth_DelEste'
        self.carpeta_documentos_trabajos_kwkrei = 'SDR_Documentos_Kenworth_KREI'
        self.carpeta_documentos_trabajos_kwrb = 'SDR_Documentos_Kenworth_RioBravo'
        self.directorio_raiz = os.path.expanduser(f'~{self.separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
        self.documentos_carpeta = "Documentos"
        self.documento_rutas_json = "Rutas_carga_destino.json"
        self.ruta_Kenworth_kwsonora = os.path.join(self.directorio_raiz, self.carpeta_documentos_trabajos_sonora,self.documentos_carpeta,self.documento_rutas_json)
        self.ruta_Kenworth_kweste = os.path.join(self.directorio_raiz, self.carpeta_documentos_trabajos_kweste,self.documentos_carpeta,self.documento_rutas_json)
        self.ruta_Kenworth_kwkrei = os.path.join(self.directorio_raiz, self.carpeta_documentos_trabajos_kwkrei,self.documentos_carpeta,self.documento_rutas_json)
        self.ruta_Kenworth_kwrb = os.path.join(self.directorio_raiz, self.carpeta_documentos_trabajos_kwrb,self.documentos_carpeta,self.documento_rutas_json)
        self.ruta_deapoyo_kwsonora = self.ruta_documentos.replace('\\','/')
        self.ruta_deapoyo_kweste = self.ruta_documentos.replace('\\','/')
        self.ruta_deapoyo_kwkrei = self.ruta_documentos.replace('\\','/')
        self.ruta_deapoyo_kwrb = self.ruta_documentos.replace('\\','/')
