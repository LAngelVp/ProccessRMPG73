#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
from datetime import *
from webbrowser import *
import calendar
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class Variables():
    separador = os.sep
    carpeta_documentos_trabajos = 'SDR_Documentos_Kenworth_KREI'
    # carpetas personales de Kenworth Rio Bravo
    documentos_Trabajos= "Trabajos"
    documentos_originales = "Original"
    documentos_Errores = "Errores"
    documentos_Procesados = "Exitosos"
    directorio_raiz = os.path.expanduser(f'~{separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
    ruta_Kenworth = os.path.join(directorio_raiz, carpeta_documentos_trabajos)
    ruta_Trabajos = os.path.join(ruta_Kenworth, documentos_Trabajos)
    ruta_original = os.path.join(ruta_Kenworth, documentos_originales)
    ruta_errores = os.path.join(ruta_Kenworth, documentos_Errores)
    ruta_exitosos = os.path.join(ruta_Kenworth, documentos_Procesados)
    ruta_documentos = os.path.join(ruta_Kenworth, "Documentos")

    #--------------------------------
    #NOTE Reemplazamos las diagonales de las rutas, con la finalidad que cualquier sistema operativo pueda ejecutar el software.
    ruta_carpeta = ruta_Kenworth.replace('\\','/')
    ruta_Trabajo = ruta_Trabajos.replace('\\','/')
    ruta_origina = ruta_original.replace('\\', '/')
    ruta_error = ruta_errores.replace('\\','/')
    ruta_procesados = ruta_exitosos.replace('\\','/')
    ruta_deapoyo = ruta_documentos.replace('\\','/')
    #________________________________________________

    pdf = 'https://onedrive.live.com/?cid=C903C3E707BD874A&id=C903C3E707BD874A%21220&parId=root&o=OneUp' #NOTE Direccion en donde se encuentra el archivo de apoyo

    #________________________________________________
    #NOTE VARIABLES PARA PROCESOS CON LA FECHA.

    # Fecha para insertar en columnas.
    # NOTE Obtenemos la fecha de hoy
    fecha_hoy = datetime.now()
    # NOTE Damos a formato de fecha en python
    FechaHoy = f'{fecha_hoy.day}/{fecha_hoy.month}/{fecha_hoy.year}'
    # NOTE Damos a formato de fecha para pandas
    fechaInsertar = datetime.strptime(FechaHoy, "%d/%m/%Y")

    def FechaExternsionGuardar(self):
        datoAdicional = datetime.now()
        fechaPath = datoAdicional.strftime('%d-%m-%Y-%H-%M-%S') #NOTE Fecha para adicionar al nombre del archivo procesado.
        return fechaPath
    
    def nombre_mes(self):
        mes_actual = datetime.now().month
        mes_actual_nombre = calendar.month_name[mes_actual].capitalize()
        return mes_actual_nombre
    
    def nombre_mes_actual_abreviado(self):
        mes_actual = datetime.now()
        mes_abreviado = mes_actual.strftime(f'%b-%y').replace(".","")
        return mes_abreviado
    
    def fechaHoy(self):
        fecha = datetime.now()
        return fecha