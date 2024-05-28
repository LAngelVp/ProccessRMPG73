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
from dateutil import parser
from openpyxl import *

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class Variables:
    def __init__(self):

#comment: variables for a date
        # Fecha para insertar en columnas.
        # NOTE Obtenemos la fecha de hoy
        self.fecha_hoy = datetime.now()
        # NOTE Damos a formato de fecha en python
        self.FechaHoy = f'{self.fecha_hoy.day}/{self.fecha_hoy.month}/{self.fecha_hoy.year}'
        # NOTE Damos a formato de fecha para pandas
        self.fechaInsertar = datetime.strptime(self.FechaHoy, "%d/%m/%Y")
#comment: separator
        self.separador = os.sep
#-----------------------------------------------------------
#comment: global folder
        self.folder_global = 'KWDataProcessRMPG73'
#comment: folder name branch
        self.folder_name_kwrb = 'RMPG_ConcesionarioKenworthRioBravo'
        self.folder_name_kwe = 'RMPG_ConcesionarioKenworthdelEste'
        self.folder_name_kwkrei = 'RMPG_ConcesionarioKREI'
        self.folder_name_kwsonora = 'RMPG_ConcesionarioKenworthSonora'
#-----------------------------------------------------------
#comment: folder name for files (general branches)
        self.documentos_Trabajos = "Trabajos"
        self.documentos_originales = "Original"
        self.documentos_Errores = "Errores"
        self.documentos_Procesados = "Exitosos"
        self.help_documents_directory = "HelpDocumetsPrivate"
#-----------------------------------------------------------
#comment: Global Document Names
        self.customer_payment_goals_file = 'CustomerPaymentGoals.json'
        self.document_saving_paths_file = 'DocumentSavingPaths.json'
        self.movement_date_document_file = 'DateMovemment.json'
        self.vendor_service_departments_file = 'Vendedores_servicio_departamentos.json'
        self.vendor_parts_departments_file = 'Vendedores_refacciones_departamentos.json'
        self.large_clients_parts_file = 'clientes_grandes.json'
        self.parts_brands_file = 'marcas_refacciones.json'

#-----------------------------------------------------------
#comment: root directory system
        self.root_directory_system = os.path.expanduser(f'~{self.separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
        self.global_route_project = os.path.join(self.root_directory_system, self.folder_global).replace('\\','/')
#-----------------------------------------------------------
#comment: root directory kw
        self.route_kwrb = os.path.join(self.global_route_project, self.folder_name_kwrb).replace('\\','/')
        self.route_kwe = os.path.join(self.global_route_project, self.folder_name_kwe).replace('\\','/')
        self.route_kwkrei = os.path.join(self.global_route_project, self.folder_name_kwkrei).replace('\\','/')
        self.route_kwsonora = os.path.join(self.global_route_project, self.folder_name_kwsonora).replace('\\','/')
#-----------------------------------------------------------
#comment: work routes kwrb
        self.ruta_Trabajos_kwrb = os.path.join(self.route_kwrb, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwrb = os.path.join(self.route_kwrb, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwrb = os.path.join(self.route_kwrb, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwrb = os.path.join(self.route_kwrb, self.documentos_Procesados).replace('\\','/')

#-----------------------------------------------------------
#comment: work routes kwe
        self.ruta_Trabajos_kwe = os.path.join(self.route_kwe, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwe = os.path.join(self.route_kwe, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwe = os.path.join(self.route_kwe, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwe = os.path.join(self.route_kwe, self.documentos_Procesados).replace('\\','/')

#-----------------------------------------------------------
#comment: work routes krei
        self.ruta_Trabajos_krei = os.path.join(self.route_kwkrei, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_krei = os.path.join(self.route_kwkrei, self.documentos_originales).replace('\\','/')
        self.ruta_errores_krei = os.path.join(self.route_kwkrei, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_krei = os.path.join(self.route_kwkrei, self.documentos_Procesados).replace('\\','/')
#-----------------------------------------------------------
#comment: work routes sonora
        self.ruta_Trabajos_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwsonora = os.path.join(self.route_kwsonora, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Procesados).replace('\\','/')
#-----------------------------------------------------------
#comment: global documents
        self.help_directory = os.path.join(self.global_route_project, self.help_documents_directory).replace('\\','/')
        self.customerPaymentGoals = os.path.join(self.help_directory, self.customer_payment_goals_file).replace('\\','/')
        self.documentSavingPaths = os.path.join(self.help_directory, self.document_saving_paths_file).replace('\\','/')
        #fecha movimiento
        self.movement_date_document = os.path.join(self.help_directory,  self.movement_date_document_file).replace('\\','/')
        #kwe
        self.nombre_documento_clasificacion_vendedores_servicio_kwe = os.path.join(self.help_directory, self.vendor_service_departments_file).replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_refacciones_kwe = os.path.join(self.help_directory, self.vendor_parts_departments_file).replace('\\','/')
        self.tamaño_clientes_refacciones_kwe = os.path.join(self.help_directory, self.large_clients_parts_file).replace('\\','/')
        self.marcas_refacciones_kwe = os.path.join(self.help_directory, self.parts_brands_file).replace('\\','/')

        self.successfulPathDirectory = {
            "KWRB" : self.ruta_exitosos_kwrb,
            "KWESTE" : self.ruta_exitosos_kwe,
            "KWKREI" : self.ruta_exitosos_krei,
            "KWSON" : self.ruta_exitosos_kwsonora,
        }



#comment: help document
        self.pdf = 'https://docs.google.com/document/d/1-TeaeWdGAXUGls18b_hH6qG-Ur1PqDznsWS8X9FPD_M/edit?usp=sharing' #NOTE Direccion en donde se encuentra el archivo de apoyo


#-----------------------------------------------------------
#comment: reading documents
    #* lectura de la fecha movimiento 
    def date_movement_config_document(self):
        document = pd.read_json(self.movement_date_document)
        date_movement = pd.to_datetime(document.loc[0,"Date_Movement"], format="%d/%m/%Y") 
        return date_movement
    #* comprobar existencia de rutas para procesar los reportes
    def comprobar_reporte_documento_rutas(self, nombre = None, concesionario = None):
        normalName = nombre.split(".")[0]
        archivo = pd.read_json(self.documentSavingPaths)
        nombre_arreglado_csv = f'{concesionario}_{normalName}_RMPG_{self.FechaExternsionGuardar()}.csv'
        nombre_arreglado_xlsx = f'{concesionario}_{normalName}_RMPG_{self.FechaExternsionGuardar()}.xlsx'
        self.docu =None
        self.docu_nombre = None
        for index, fila in archivo.iterrows():
            if (fila["nombre"] == nombre):
                self.docu_nombre = fila["nombre"]
                self.docu = str(fila["path"])
                break
        if (self.docu is not None) | (self.docu_nombre == nombre):
            return os.path.join(self.docu,nombre_arreglado_csv)
        else:
            if (concesionario in self.successfulPathDirectory):
                return os.path.join(self.successfulPathDirectory[concesionario],nombre_arreglado_xlsx)
            else:
                pass
#-----------------------------------------------------------

#comment: save document    
    def guardar_datos_dataframe(self, nombre_documento, dataframe, concesionario = None):
        if (os.path.basename(self.comprobar_reporte_documento_rutas(nombre_documento, concesionario)).split(".")[1] == nombre_documento.split(".")[1]):
                dataframe.to_excel(self.comprobar_reporte_documento_rutas(nombre_documento, concesionario), engine='openpyxl', index=False )
        else:
            dataframe.to_csv(self.comprobar_reporte_documento_rutas(nombre_documento, concesionario), encoding="utf-8", index=False )

#-----------------------------------------------------------
#comment: functions

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
    
    def nombre_mes_base_columna(self, valor):
        mes = valor.strftime(f'%b-%y').replace(".","")
        return mes
    
    def parse_date_safe(self, date_str):
        try:
            # Parsear la cadena a un objeto datetime
            parsed_date = parser.parse(date_str, dayfirst=True)
            if parsed_date:
                # Obtener solo la parte de la fecha (eliminando hora, minuto y segundo)
                date_only = parsed_date.date()
                datetime_with_midnight = parser.parse(str(date_only))
                return datetime_with_midnight
            else:
                return None
        except (parser.ParserError, TypeError, ValueError):
            return None
        
# important : Formato de fecha {{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}
    #! FORMATO PARA PODER HACER OPERACIONES CON LAS FECHAS
    def global_date_format_america(self, data, name_column=None):
        if name_column in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[name_column]):
                try:
                    data[name_column] = pd.to_datetime(data[name_column]).dt.date
                    data[name_column] = pd.to_datetime(data[name_column], dayfirst=True)
                except:
                    pass
            elif pd.api.types.is_object_dtype(data[name_column]):
                    data[name_column] = data[name_column].astype(str)
                    data[name_column] = data[name_column].apply(self.parse_date_safe)
            else:
                pass
        return data
    
    #! FORMATO PARA MES/DIA/AÑO
    def global_date_format_mdy_america(self, data, name_column=None):
        if name_column in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[name_column]) or pd.api.types.is_object_dtype(data[name_column]):
                data[name_column] = data[name_column].apply(lambda x: x.strftime("%m/%d/%Y") if not pd.isnull(x) else pd.NaT)
            else:
                pass
        return data
    
    #! FORMATO PARA DIA/MES/AÑO
    def global_date_format_dmy_mexican(self, data, name_column=None):
        if name_column in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[name_column]) or pd.api.types.is_object_dtype(data[name_column]):
                data[name_column] = data[name_column].apply(lambda x: x.strftime("%d/%m/%Y") if not pd.isnull(x) else pd.NaT)
            else:
                pass
        return data
#// {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

# comment: CLASIFICACIONES DE VENDEDORES KWESTE
    def clasificacion_vendedores_departamentos_refacciones(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_refacciones_kwe)
        return documento
    def clasificacion_tamaño_clientes_refacciones(self):
        documento = pd.read_json(self.tamaño_clientes_refacciones_kwe)
        return documento
    def marcas_refacciones_fun(self):
        documento = pd.read_json(self.marcas_refacciones_kwe)
        return documento
    def vendedores_y_depas_este_servicio(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_servicio_kwe)
        return documento