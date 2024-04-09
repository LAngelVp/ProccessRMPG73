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
import json
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class Variables():
    def __init__(self):
        self.separador = os.sep
        self.carpeta_documentos_trabajos = 'SDR_Documentos_Kenworth_DelEste'
        # carpetas personales de Kenworth Rio Bravo
        self.documentos_Trabajos = "Trabajos"
        self.documentos_originales = "Original"
        self.documentos_Errores = "Errores"
        self.documentos_Procesados = "Exitosos"
#{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}        
#COMMENT: NOMBRE DE LOS DOCUMENTOS DE APOYO
        self.nombre_documento_clasificacion_vendedores_refacciones = "Vendedores_refacciones_departamentos.json"
        self.nombre_documento_clasificacion_vendedores_servicio = "Vendedores_servicio_departamentos.json"
#{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}        

        self.directorio_raiz = os.path.expanduser(f'~{self.separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
        self.ruta_Kenworth = os.path.join(self.directorio_raiz, self.carpeta_documentos_trabajos)
        self.ruta_Trabajos = os.path.join(self.ruta_Kenworth, self.documentos_Trabajos)
        self.ruta_original = os.path.join(self.ruta_Kenworth, self.documentos_originales)
        self.ruta_errores = os.path.join(self.ruta_Kenworth, self.documentos_Errores)
        self.ruta_exitosos = os.path.join(self.ruta_Kenworth, self.documentos_Procesados)
        self.ruta_documentos = os.path.join(self.ruta_Kenworth, "Documentos")
        self.route_file_date = os.path.join(self.ruta_documentos, "Config_Document.json")
        self.ruta_documentos_rutas = os.path.join(self.ruta_documentos, "Rutas_Envio.json")
        self.vendedores_servicio_detallado_este = os.path.join(self.ruta_documentos, "Vendedores_Servicio_Detallado_Este.json")
    
        self.clasif_vendedores_refacciones = os.path.join(self.ruta_documentos, "Clasificacion_Vendedores_refacc.json")
        self.tamaño_clientes_refacciones = os.path.join(self.ruta_documentos, "clientes_grandes.json")
        self.marcas_refacciones = os.path.join(self.ruta_documentos, "marcas_refacciones")

        #--------------------------------
        #NOTE Reemplazamos las diagonales de las rutas, con la finalidad que cualquier sistema operativo pueda ejecutar el software.
        self.ruta_carpeta = self.ruta_Kenworth.replace('\\','/')
        self.ruta_Trabajo = self.ruta_Trabajos.replace('\\','/')
        self.ruta_origina = self.ruta_original.replace('\\', '/')
        self.ruta_error = self.ruta_errores.replace('\\','/')
        self.ruta_procesados = self.ruta_exitosos.replace('\\','/')
        self.ruta_deapoyo = self.ruta_documentos.replace('\\','/')
        self.route_file_date_movement  = self.route_file_date.replace('\\','/')
        self.ruta_envio_documentos  = self.ruta_documentos_rutas.replace('\\','/')
        self.ruta_vendedores_servicio_detallado_este  = self.vendedores_servicio_detallado_este.replace('\\','/')

        self.clasif_de_vendedores_refacciones  = self.clasif_vendedores_refacciones.replace('\\','/')
        self.tamaño_de_clientes_refacciones  = self.tamaño_clientes_refacciones.replace('\\','/')
        self.marcas_de_refacciones  = self.marcas_refacciones.replace('\\','/')
        
        #________________________________________________

        self.pdf = 'https://onedrive.live.com/?cid=C903C3E707BD874A&id=C903C3E707BD874A%21220&parId=root&o=OneUp' #NOTE Direccion en donde se encuentra el archivo de apoyo

        #________________________________________________
        #NOTE VARIABLES PARA PROCESOS CON LA FECHA.

        # Fecha para insertar en columnas.
        # NOTE Obtenemos la fecha de hoy
        self.fecha_hoy = datetime.now()
        # NOTE Damos a formato de fecha en python
        self.FechaHoy = f'{self.fecha_hoy.day}/{self.fecha_hoy.month}/{self.fecha_hoy.year}'
        # NOTE Damos a formato de fecha para pandas
        self.fechaInsertar = datetime.strptime(self.FechaHoy, "%d/%m/%Y")

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
    
    def date_movement_config_document(self):
        document = pd.read_json(self.route_file_date)
        date_movement = pd.to_datetime(document.loc[0,"Date_Movement"], format="%d/%m/%Y", errors="coerce") 
        return date_movement
    
    def comprobar_reporte_documento_rutas(self, nombre=None):
        archivo = pd.read_json(self.ruta_envio_documentos)
        nombre_arreglado_csv = f'KWESTE_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.csv'
        nombre_arreglado_xlsx = f'KWESTE_{nombre.split(".")[0]}_RMPG_{self.FechaExternsionGuardar()}.xlsx'
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
        
    def vendedores_y_depas_este_servicio(self):
        documento = pd.read_json(self.ruta_vendedores_servicio_detallado_este)
        return documento
# SEPARATOR: CLASIFICACIONES DE VENDEDORES KWESTE
    def clasificacion_vendedores_departamentos_refacciones(self):
        documento = pd.read_json(self.clasif_de_vendedores_refacciones)
        return documento
    def clasificacion_tamaño_clientes_refacciones(self):
        documento = pd.read_json(self.tamaño_de_clientes_refacciones)
        return documento
    def marcas_refacciones_fun(self):
        documento = pd.read_json(self.marcas_de_refacciones)
        return documento
#------------
    def guardar_datos_dataframe(self, nombre_documento, dataframe):
        if (os.path.basename(self.comprobar_reporte_documento_rutas(nombre_documento)).split(".")[1] == nombre_documento.split(".")[1]):
                dataframe.to_excel(self.comprobar_reporte_documento_rutas(nombre_documento), index=False )
        else:
            dataframe.to_csv(self.comprobar_reporte_documento_rutas(nombre_documento), encoding="utf-8", index=False )
    
