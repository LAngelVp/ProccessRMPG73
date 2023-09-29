#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
import os
from datetime import *
from webbrowser import *
class Variables():
    separador = os.sep
    carpeta_documentos_trabajos = 'SDR_Documentos_Trabajos'
    carpeta_documentos_originales = 'SDR_Documentos_Originales'
    carpeta_documentos_errores = 'SDR_Documentos_Error'
    carpeta_documentos_Procesados = 'SDR_Documentos_Procesados'
    # carpetas personales de Kenworth Rio Bravo
    documentos_Trabajos_kwrb = "Kenworth_RioBravo_Trabajos"
    documentos_originales_kwrb = "Kenworth_RioBravo_Originales"
    documentos_Errores_kwrb = "Kenworth_RioBravo_Error"
    documentos_Procesados_kwrb = "Kenworth_RioBravo_Procesados"
    directorio_raiz = os.path.expanduser(f'~{separador}') #NOTE Obtenemos la ruta raiz del sistema, con raiz en el usuario.
    ruta_Kenworth_RioBravo = os.path.join(directorio_raiz, "SDR_Documentos_Kenworth_RioBravo")
    ruta_Trabajos = os.path.join(ruta_Kenworth_RioBravo, "Trabajos")
    ruta_original = os.path.join(ruta_Kenworth_RioBravo, "Original")
    ruta_errores = os.path.join(ruta_Kenworth_RioBravo, "Errores")
    ruta_exitosos = os.path.join(ruta_Kenworth_RioBravo, "Exitosos")
    ruta_documentos = os.path.join(ruta_Kenworth_RioBravo, "Documentos")
    # RT = f'{directirio_raiz}{carpeta_documentos_trabajos}{separador}{documentos_Trabajos_kwrb}' #NOTE Ruta de la carpeta en donde se almacenaran los reportes que se van a trabajar.
    # RO = f'{directirio_raiz}{carpeta_documentos_originales}{separador}{documentos_originales_kwrb}' #NOTE Lugar donde se van a mandar los documentos originales.
    # RE = f'{directirio_raiz}{carpeta_documentos_errores}{separador}{documentos_Errores_kwrb}'   #NOTE Ruta de la carpeta donde se almacenaran los reportes con errores de nombre.
    # RP = f'{directirio_raiz}{carpeta_documentos_Procesados}{separador}{documentos_Procesados_kwrb}' #NOTE Ruta de la carpeta donde se almacenaran los reportes realizados con exito.
    #--------------------------------
    #NOTE Reemplazamos las diagonales de las rutas, con la finalidad que cualquier sistema operativo pueda ejecutar el software.
    ruta_carpeta_KWRioBravo = ruta_Kenworth_RioBravo.replace('\\','/')
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
# OBTENERMOS EL PRIMER DIA DEL MES.
    primerDiaMes = fecha_hoy.replace(day=1)
    
    def FechaExternsionGuardar(self):
        datoAdicional = datetime.now()
        fechaPath = datoAdicional.strftime('%d-%m-%Y-%H-%M-%S') #NOTE Fecha para adicionar al nombre del archivo procesado.
        return fechaPath
    
    def fechaHoy(self):
        fecha = datetime.now()
        return fecha