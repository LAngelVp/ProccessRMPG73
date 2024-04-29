#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import json
import os
from datetime import *
from webbrowser import *
import calendar
import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class Variables():
    def __init__(self):
#! variables for a date
        # Fecha para insertar en columnas.
        # NOTE Obtenemos la fecha de hoy
        self.fecha_hoy = datetime.now()
        # NOTE Damos a formato de fecha en python
        self.FechaHoy = f'{self.fecha_hoy.day}/{self.fecha_hoy.month}/{self.fecha_hoy.year}'
        # NOTE Damos a formato de fecha para pandas
        self.fechaInsertar = datetime.strptime(self.FechaHoy, "%d/%m/%Y")
#! separator
        self.separador = os.sep
#{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}
#? folder name branch
        self.carpeta_documentos_trabajos = 'SDR_Documentos_Kenworth_RioBravo'
        self.folder_name_kwrb = 'SDR_Documentos_Kenworth_RioBravo'
        self.folder_name_kwe = 'SDR_Documentos_Kenworth_DelEste'
#{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}
        #? folder name for files (general branches)
        self.documentos_Trabajos = "Trabajos"
        self.documentos_originales = "Original"
        self.documentos_Errores = "Errores"
        self.documentos_Procesados = "Exitosos"
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! root directory system
        self.root_directory_system = os.path.expanduser(f'~{self.separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! root directory kw
        self.route_kwrb = os.path.join(self.root_directory_system, self.folder_name_kwrb)
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! work routes kwrb
        self.ruta_Trabajos_kwrb = os.path.join(self.route_kwrb, self.documentos_Trabajos)
        self.ruta_original_kwrb = os.path.join(self.route_kwrb, self.documentos_originales)
        self.ruta_errores_kwrb = os.path.join(self.route_kwrb, self.documentos_Errores)
        self.ruta_exitosos_kwrb = os.path.join(self.route_kwrb, self.documentos_Procesados)
        self.ruta_documentos_kwrb = os.path.join(self.route_kwrb, "Documentos")
        self.route_file_date_kwrb = os.path.join(self.ruta_documentos_kwrb, "Config_Document.json")
        self.ruta_documentos_rutas_kwrb = os.path.join(self.ruta_documentos_kwrb, "Rutas_Envio.json")
        #--------------------------------
        #NOTE Reemplazamos las diagonales de las rutas, con la finalidad que cualquier sistema operativo pueda ejecutar el software.
        self.ruta_carpeta_kwrb = self.route_kwrb.replace('\\','/')
        self.ruta_Trabajo_kwrb = self.ruta_Trabajos_kwrb.replace('\\','/')
        self.ruta_origina_kwrb = self.ruta_original_kwrb.replace('\\', '/')
        self.ruta_error_kwrb = self.ruta_errores_kwrb.replace('\\','/')
        self.ruta_procesados_kwrb = self.ruta_exitosos_kwrb.replace('\\','/')
        self.ruta_deapoyo_kwrb = self.ruta_documentos_kwrb.replace('\\','/')
        self.route_file_date_movement_kwrb  = self.route_file_date_kwrb.replace('\\','/')
        self.ruta_envio_documentos_kwrb  = self.ruta_documentos_rutas_kwrb.replace('\\','/')
#{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}




#! help document
        self.pdf = 'https://docs.google.com/document/d/1-TeaeWdGAXUGls18b_hH6qG-Ur1PqDznsWS8X9FPD_M/edit?usp=sharing' #NOTE Direccion en donde se encuentra el archivo de apoyo
        #________________________________________________

#{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}
#? reading documents
    def date_movement_config_document(self):
        document = pd.read_json(self.route_file_date_movement_kwrb)
        date_movement = pd.to_datetime(document.loc[0,"Date_Movement"], format="%d/%m/%Y") 
        return date_movement

    def comprobar_reporte_documento_rutas(self, nombre=None):
        archivo = pd.read_json(self.ruta_envio_documentos)
        nombre_arreglado_csv = f'KWRB_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.csv'
        nombre_arreglado_xlsx = f'KWRB_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.xlsx'
        self.docu =None
        self.docu_nombre = None
        for index, fila in archivo.iterrows():
            if (fila["Nombre_documento"] == nombre):
                self.docu_nombre = fila["Nombre_documento"]
                self.docu = str(fila["Ruta_destino_documento"])
                break
        if (self.docu is not None) | (self.docu_nombre == nombre):
            return os.path.join(self.docu,nombre_arreglado_csv)
        else:
            return os.path.join(self.ruta_procesados,nombre_arreglado_xlsx)
#{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}
    
#! save document    
    def guardar_datos_dataframe(self, nombre_documento, dataframe):
        if (os.path.basename(self.comprobar_reporte_documento_rutas(nombre_documento)).split(".")[1] == nombre_documento.split(".")[1]):
                dataframe.to_excel(self.comprobar_reporte_documento_rutas(nombre_documento), index=False )
        else:
            dataframe.to_csv(self.comprobar_reporte_documento_rutas(nombre_documento), encoding="utf-8", index=False )

#{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}
#! functions
    def FechaExternsionGuardar(self):
        datoAdicional = datetime.now()
        fechaPath = datoAdicional.strftime('%d-%m-%Y-%H-%M-%S') #NOTE Fecha para adicionar al nombre del archivo procesado.
        return fechaPath
    
    def nombre_mes(self):
        mes_actual = self.date_movement_config_document().month
        mes_actual_nombre = calendar.month_name[mes_actual].capitalize()
        return mes_actual_nombre
    
    def nombre_mes_actual_abreviado(self):
        mes_actual = self.date_movement_config_document()
        mes_abreviado = mes_actual.strftime(f'%b-%y').replace(".","")
        return mes_abreviado
    
    def fechaHoy(self):
        fecha = datetime.now()
        return fecha
    
    
        