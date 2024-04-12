#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
import threading
from resources import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from webbrowser import *
from .Logica_Reportes.Variables.ContenedorVariables import Variables
from .Inicio_FechaMovimiento import *
from .KenworthConnect import *
from .InicialClassObjetivos import *
from .UI.V_KWESTE import *
from .Home_rutas import *
from .Vendedores import *
from ..mensajes_alertas import Mensajes_Alertas
import subprocess

class Home_KWESTE(QMainWindow, QDialog, Variables):
    def __init__(self):
        super(Home_KWESTE,self).__init__()
        # variables a las rutas de los iconos e imagenes
        Icon_Cerrar = QIcon(":/Source/Icon_Close.png")
        Icon_Minimizar = QIcon(":/Source/Icon_Minimize.png")
        Icon_Help = QIcon(":/Source/Icon_Help.png")
        Icon_Delete = QIcon(":/Source/Icon_Delete.png")
        Icon_Proccess = QIcon(":/Source/Icon_Proccess.png")
        Icon_Upload = QIcon(":/Source/Icon_Upload.png")
        logo_KWESTE = QPixmap(":/Source/KWESTE.png")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        
        # llamamos el metodo de creacion de carpetas
        self.Creacion_Carpetas()
        # quitamos la barra superior
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Crear la instancia de la ventana y configurarla
        self.ventKWESTE = Ui_Kenworth_del_Este()
        self.ventKWESTE.setupUi(self)
        # colocar los iconos e imagenes en su correspondiente elemento.
        self.ventKWESTE.lblLogoKWESTE.setPixmap(logo_KWESTE)
        self.ventKWESTE.btc_btc_Cerrar.setIcon(Icon_Cerrar)
        self.ventKWESTE.btc_btc_Minimizar.setIcon(Icon_Minimizar)
        self.ventKWESTE.btn_btn_Ayuda.setIcon(Icon_Help)
        self.ventKWESTE.btn_btn_Eliminar.setIcon(Icon_Delete)
        self.ventKWESTE.btn_btn_Eliminar.setIconSize(QtCore.QSize(24, 24))
        self.ventKWESTE.btn_btn_Comenzar.setIcon(Icon_Proccess)
        self.ventKWESTE.btn_btn_Comenzar.setIconSize(QtCore.QSize(24, 24))
        self.ventKWESTE.btn_btn_Subir.setIcon(Icon_Upload)
        self.ventKWESTE.btn_btn_Subir.setIconSize(QtCore.QSize(24, 24))
        # creamos el hilo
        self.Hilo = trabajohilo()
        #conexiones de los botones
        self.ventKWESTE.btn_btn_Subir.clicked.connect(self.Cargar)
        self.ventKWESTE.btn_btn_Comenzar.clicked.connect(self.ComenzarProceso)
        self.ventKWESTE.btn_btn_Eliminar.clicked.connect(self.RemoveProcessed)
        self.ventKWESTE.btn_btn_Ayuda.clicked.connect(self.Ayuda)
        self.ventKWESTE.btc_btc_Cerrar.clicked.connect(self.Cerrar)
        self.ventKWESTE.btc_btc_Minimizar.clicked.connect(self.Minimizar)
        self.ventKWESTE.btn_btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.ventKWESTE.btn_btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.ventKWESTE.btn_btn_Procesados.clicked.connect(self.abrir_ruta_procesados)

        # MENU DE OPCIONES
        self.ventKWESTE.actionObjetivos_Mensuales_PagosClientes.triggered.connect(self.ObjetivosPagoClientes)
        self.ventKWESTE.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)
        self.ventKWESTE.actionDirecciones_de_envio.triggered.connect(self.direcciones_envio)
        self.ventKWESTE.actionDepartamentos.triggered.connect(self.departamentos_vendedores)

        # señales del hilo
        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)
        

        Home_DateMovement()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    

    def Aceptar_callback(self):
        pass
    def Ayuda_callback(self):
        open_new(Variables().pdf)

    def departamentos_vendedores(self):
        self.ventana_departamentos = Vendedores()
        self.ventana_departamentos.show()

    def direcciones_envio(self):
        self.ventana_rutas = rutas()
        self.ventana_rutas.show()

    def ObjetivosPagoClientes(self):
        self.ventana_obj = ClassPrincipalObjPagos()
        self.ventana_obj.show()

    def FechaMovimiento(self):
        self.ventana_obj = Home_DateMovement()
        self.ventana_obj.show()

    def abrir_ruta_errores(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', Variables().ruta_errores, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                print("Error al abrir el archivo con Excel:", e)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_originales(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', Variables().ruta_origina, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                print("Error al abrir el archivo con Excel:", e)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_procesados(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', Variables().ruta_procesados, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                print("Error al abrir el archivo con Excel:", e)

        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def mensajeTrabajoTerminado(self):
        Mensajes_Alertas(
            "Trabajos Terminados",
            "Todos los trabajos que se comenzaron fueron insertados por el proceso lógico del sistema.",
            QMessageBox.Information,
            None,
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        textoVacio =""
        self.nombreArchivoTrabajando(textoVacio)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#-------------------------------------------------


    def mensajeArchivoErroneo(self, mensaje):
        Mensajes_Alertas(
            "Errores durante el proceso",
            f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {Variables().ruta_error}',
            QMessageBox.Critical,
            "Cuando el sistema muestra un error como este, existen algunos factores que se tienen que tomar en cuenta:\n1.- El nombre del documento no tiene la nomenclatura correcta.\n2.- El documento original no contiene las columnas a trabajar o su contendo es incorrecto.\n3.- EL documento no es el correcto o esta corrupto.",
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
# MOSTRAR NOMBRE DEL DOCUMENTO QUE SE ESTA TRABAJANDO
    def nombreArchivoTrabajando(self, nombre):
        if (nombre != ""):
            self.ventKWESTE.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.ventKWESTE.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.ventKWESTE.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.ventKWESTE.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
#-------------------------------------------------------
# EVENTOS DEL MOUSE
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    # Apartado de funciones
    #-------------------------
    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(Variables().ruta_Trabajo)
        self.ventKWESTE.Tabla_cola.setRowCount(len(archivos_para_mostrar))
        self.ventKWESTE.Tabla_cola.setColumnCount(1)
        self.ventKWESTE.Tabla_cola.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ventKWESTE.Tabla_cola.setItem(fila, 0, elemento)
            # font = QtGui.QFont()
            # font.setPointSize(30)  # Establece el tamaño de la letra a 14 puntos
            # elemento.setFont(font)
        # self.ventKWESTE.Tabla_cola.setColumnWidth(0, 415)
        header = self.ventKWESTE.Tabla_cola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Procesado(self):
        archivos_para_mostrar = os.listdir(Variables().ruta_procesados)
        self.ventKWESTE.Tabla_Procesados.setRowCount(len(archivos_para_mostrar))
        self.ventKWESTE.Tabla_Procesados.setColumnCount(1)
        self.ventKWESTE.Tabla_Procesados.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ventKWESTE.Tabla_Procesados.setItem(fila, 0, elemento)
            # font = QtGui.QFont()
            # font.setPointSize(30)  # Establece el tamaño de la letra a 14 puntos
            # elemento.setFont(font)
        # self.ventKWESTE.Tabla_Procesados.setColumnWidth(0, 415)
        header = self.ventKWESTE.Tabla_Procesados.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


    def Creacion_Carpetas(self):
        directorio = os.listdir(Variables().directorio_raiz)
        for i in directorio:
            if not os.path.exists(f'{Variables().ruta_Trabajo}'):
                os.makedirs(f'{Variables().ruta_Trabajo}')
            elif not os.path.exists(f'{Variables().ruta_origina}'):
                os.makedirs(f'{Variables().ruta_origina}')
            elif not os.path.isdir(f'{Variables().ruta_error}'):
                os.makedirs(f'{Variables().ruta_error}')
            elif not os.path.isdir(f'{Variables().ruta_procesados}'):
                os.makedirs(f'{Variables().ruta_procesados}')
            elif not os.path.isdir(f'{Variables().ruta_deapoyo}'):
                os.makedirs(f'{Variables().ruta_deapoyo}')
            else:
                pass
    # cerrar la ventana
    def Cerrar(self):
        self.close()
    # minimizar la ventana
    def Minimizar(self):
        self.showMinimized()
    # mostrar la data en las tablas
    
    # cargar los archivos a la carpeta de trabajo
    def Cargar(self):
        self.Creacion_Carpetas()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
        ubicacion_carga = os.chdir(Variables().directorio_raiz)
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog  # Evitar el uso del diálogo nativo del sistema operativo (opcional)
        options |= QFileDialog.ReadOnly  # Permite abrir los archivos solo en modo lectura (opcional)
        options |= QFileDialog.HideNameFilterDetails  # Ocultar detalles del filtro (opcional)
        options |= QFileDialog.DontResolveSymlinks  # No resolver enlaces simbólicos (opcional)

        selected_filter = "Hojas de Excel (*.xlsx);;Todos los archivos (*)"
        
        if os.path.isdir(Variables().ruta_Trabajo) == True:
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, Variables().ruta_Trabajo)
            except:
                pass
        else:
            os.makedirs(Variables().ruta_Trabajo)
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, Variables().ruta_Trabajo)
            except:
                pass
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#----------------------------------------        
    # REALIZAR PROCESO
    # HILO DEL TRABAJO DE " KWESTE "
    def ComenzarProceso(self):
        if self.Hilo.isRunning():
            self.Hilo.requestInterruption()
        else:
            self.Hilo.start()

    def eliminar(self):
        carpeta_contenido_eliminar = os.listdir(Variables().ruta_procesados)
        for archivo in carpeta_contenido_eliminar:
            if (len(carpeta_contenido_eliminar) != 0):
                try:
                    archivo_completo = os.path.join(Variables().ruta_procesados, archivo)
                    os.remove(archivo_completo)
                except:
                    pass
            else:
                pass

    # eliminamos los trabajos realizados de la carpeta de exitosos.
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(Variables().ruta_procesados)
        if (len(ruta_trabajos_procesados) == 0):
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.Aceptar_callback)]).Eliminar_vacio
        else:
            Mensajes_Alertas(None,None,None,None,botones=[("Eliminar", self.eliminar)]).Eliminar_lleno
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()


    def Ayuda(self):
        Mensajes_Alertas(
            "Información de Ayuda",
            'Si tienes problemas con la aplicación debido a que no sabes como guardar tus archivos de excel para que puedan ser transformados.\nPuedes ver el manual de usuario dando click en el boton de "Ver"',
            QMessageBox.Information,  # Aquí se pasa el tipo de ícono
            None,
            botones = [
                ("Aceptar", self.Aceptar_callback),
                ("Ver", self.Ayuda_callback)
            ]
        ).Apartado_Ayuda
        
        

# CLASE DEL HILO----------------------
class trabajohilo(QThread, Variables):
# agregamos una variable de tipo señal
    signal = pyqtSignal()
    signalDocumentosErroneos = pyqtSignal(str)
    signalShowTrabajos = pyqtSignal()
    signalShowProcesados = pyqtSignal()
    signalNombreArchivo =  pyqtSignal(str)

    def run(self):
        array_errores = []
        #---------------------------------------
        # diccionario de los archivos.
        diccionario_archivos = {
            "CE.xlsx" : KenworthConnect().Credito,
            "ICE.xlsx" : KenworthConnect().Inventario,
            "BOE.xlsx" : KenworthConnect().BackOrders,
            "SVE.xlsx" : KenworthConnect().SalidasEnVale,
            "SCE.xlsx" : KenworthConnect().SeguimientoCores,
            "OSE.xlsx" : KenworthConnect().OrdenesDeServicio,
            "TEE.xlsx" : KenworthConnect().TrabajosPorEstado,
            "PCE.xlsx" : KenworthConnect().PagoClientes,
            "CDE.xlsx" : KenworthConnect().Compras,
            "IUE.xlsx" : KenworthConnect().InventarioUnidades,
            "SDE.xlsx" : KenworthConnect().ServicioDetallado,
            "RE.xlsx" : KenworthConnect().Refacciones,
            "RFE.xlsx" : KenworthConnect().ResultadosFinancieros
        }
        #-----------------------------------------------
        while True:
            carpeta_de_trabajos = os.listdir(Variables().ruta_Trabajo)
            if not carpeta_de_trabajos:
                nombre_documento = ""
                self.signalNombreArchivo.emit(nombre_documento)
                return
            else:
                for nombre_archivo in carpeta_de_trabajos:
                    if (nombre_archivo in diccionario_archivos):
                        try:
                            self.signalNombreArchivo.emit(nombre_archivo)
                            Metodo = diccionario_archivos[nombre_archivo]
                            Metodo()
                            self.Comprobacion_Originales(nombre_archivo)
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                        except Exception as e:
                            array_errores.append(nombre_archivo)
                            self.Comprobacion_Errores(nombre_archivo)
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                            continue
                    else:
                        nombre_archivo_error = nombre_archivo
                        array_errores.append(nombre_archivo_error)
                        self.Comprobacion_Errores(nombre_archivo)
                        self.signalShowTrabajos.emit()
                        self.signalShowProcesados.emit()
                        continue
                self.signalShowTrabajos.emit()
                self.signalShowProcesados.emit()
            if array_errores:
                mensaje = ""
                x = 1
                for i in array_errores:
                    mensaje += f'{x}.-{i}\n'
                    x += 1
                self.signalDocumentosErroneos.emit(mensaje)
                continue
            self.signalShowTrabajos.emit()
            self.signalShowProcesados.emit()

#--------------------------------------------------
# COMPROBAR SI EXISTE EL DOCUMENTO ORIGINAL EN EL DESTINO
    def Comprobacion_Originales(self, file_name):
        ruta_origen = os.path.join(Variables().ruta_Trabajo, file_name)
        destino_archivoOriginal = os.path.join(Variables().ruta_origina, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, Variables().ruta_origina)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, Variables().ruta_origina)
#--------------------------------------------------
#--------------------------------------------------
# COMPRROBAR SI EXISTE EL DOCUMENTO ERRONEO EN EL DESTINO
    def Comprobacion_Errores(self, file_name):
        ruta_origen = os.path.join(Variables().ruta_Trabajo, file_name)
        destino_archivoOriginal = os.path.join(Variables().ruta_error, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, Variables().ruta_error)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, Variables().ruta_error)
#--------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Crear una instancia de la clase MyDialog y mostrarla
    Ventana = Home_KWESTE()
    Ventana.show()
    sys.exit(app.exec_())