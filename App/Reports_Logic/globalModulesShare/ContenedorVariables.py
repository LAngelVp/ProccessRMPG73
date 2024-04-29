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
#? global folder
        self.folder_global = 'KWDataProcessRMPG73'
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
        self.help_documents_directory = "HelpDocumetsPrivate"
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! root directory system
        self.root_directory_system = os.path.expanduser(f'~{self.separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
        self.global_route_project = os.path.join(self.root_directory_system, self.folder_global)
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! root directory kw
        self.route_kwrb = os.path.join(self.global_route_project, self.folder_name_kwrb).replace('\\','/')
        self.route_kwe = os.path.join(self.global_route_project, self.folder_name_kwe)
#{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}
#! work routes kwrb
        self.ruta_Trabajos_kwrb = os.path.join(self.route_kwrb, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwrb = os.path.join(self.route_kwrb, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwrb = os.path.join(self.route_kwrb, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwrb = os.path.join(self.route_kwrb, self.documentos_Procesados).replace('\\','/')

#{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}
#! work routes kwe
        self.ruta_Trabajos_kwe = os.path.join(self.route_kwe, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwe = os.path.join(self.route_kwe, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwe = os.path.join(self.route_kwe, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwe = os.path.join(self.route_kwe, self.documentos_Procesados).replace('\\','/')

#{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}
#? global documents
        self.help_directory = os.path.join(self.global_route_project, self.help_documents_directory).replace('\\','/')
        #fecha movimiento
        self.movement_date_document = os.path.join(self.help_directory, 'DateMovemment').replace('\\','/')
        #kwrb
        self.ruta_documentos_rutas_kwrb = os.path.join(self.help_directory, "Rutas_Envio.json").replace('\\','/')
        #kwe
        self.ruta_documentos_rutas_kwe = os.path.join(self.help_directory, "Rutas_Envio.json").replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_servicio_kwe = os.path.join(self.help_directory, "Vendedores_servicio_departamentos.json").replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_refacciones_kwe = os.path.join(self.help_directory, "Vendedores_refacciones_departamentos.json").replace('\\','/')
        self.tamaño_clientes_refacciones_kwe = os.path.join(self.help_directory, "clientes_grandes.json").replace('\\','/')
        self.marcas_refacciones_kwe = os.path.join(self.help_directory, "marcas_refacciones").replace('\\','/')




#! help document
        self.pdf = 'https://docs.google.com/document/d/1-TeaeWdGAXUGls18b_hH6qG-Ur1PqDznsWS8X9FPD_M/edit?usp=sharing' #NOTE Direccion en donde se encuentra el archivo de apoyo
        #________________________________________________

#{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}
#? reading documents
    #lectura de la fecha movimiento
    def date_movement_config_document_kwrb(self):
        document = pd.read_json(self.movement_date_document)
        date_movement = pd.to_datetime(document.loc[0,"Date_Movement"], format="%d/%m/%Y") 
        return date_movement
    #comprobar existencia de rutas para procesar los reportes
    def comprobar_reporte_documento_rutas(self, nombre=None, concesionario=None):
        if concesionario:
            ruta_concesionario = f'self.ruta_documentos_rutas_{concesionario.lower()}'
        else:
            pass
        archivo = pd.read_json(os.path.join(ruta_concesionario))
        nombre_arreglado_csv = f'{concesionario}_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.csv'
        nombre_arreglado_xlsx = f'{concesionario}_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.xlsx'
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
    
    def nombre_mes_base_columna(self, valor):
        mes = valor.strftime(f'%b-%y').replace(".","")
        return mes
    
    def global_date_format_america(self, data, name_column=None):
        if name_column in data.columns:
            if data[name_column].dtype == "datetime64[ns]":
                data[name_column] = pd.to_datetime(data[name_column],errors="coerce").dt.date
                data[name_column] = data[name_column].astype('datetime64[ns]')
            else:
                try:
                    data[name_column] = pd.to_datetime(data[name_column], format='%d/%m/%Y')
                except:
                    try:
                        data[name_column] = pd.to_datetime(data[name_column], format='%m/%d/%Y')
                    except:
                        try:
                            data[name_column] = pd.to_datetime(data[name_column], format='%Y/%m/%d')
                        except:
                            pass
        return data
    


    def global_date_format_mdy_america(self, data, name_column=None):
        if data[name_column].dtype == "datetime64[ns]":
            try:
                data[name_column] = pd.to_datetime(data[name_column], errors="coerce").dt.strftime("%m/%d/%Y")
            except:
                pass
        return data
    def global_date_format_dmy_mexican(self, data, name_column=None):
        if data[name_column].dtype == "datetime64[ns]":
            try:
                data[name_column] = pd.to_datetime(data[name_column], errors="coerce").dt.strftime("%d/%m/%Y")
            except:
                pass
        return data
    
    def vendedores_y_depas_este_servicio(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_servicio_kwe)
        return documento
# SEPARATOR: CLASIFICACIONES DE VENDEDORES KWESTE
    def clasificacion_vendedores_departamentos_refacciones(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_refacciones_kwe)
        return documento
    def clasificacion_tamaño_clientes_refacciones(self):
        documento = pd.read_json(self.tamaño_clientes_refacciones_kwe)
        return documento
    def marcas_refacciones_fun(self):
        documento = pd.read_json(self.marcas_refacciones_kwe)
        return documento