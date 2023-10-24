#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from resources import *
from PyQt5 import  *
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from datetime import *
from webbrowser import *
from .Logica_Reportes.Variables.ContenedorVariables import Variables
from .Inicio_FechaMovimiento import *
from .KenworthConnect import *
from .InicialClassObjetivos import *
from .UI.V_KWRB import *
import subprocess
class KenworthRioBravo(QMainWindow, Variables, ):
    def __init__(self):
        super(KenworthRioBravo, self).__init__()
        self.Creacion_Carpetas()
        self.ventanaRioBravo = Ui_MainWindow()
        self.ventanaRioBravo.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.ventanaRioBravo.btnAyuda.setIcon(QIcon(":/Source/Icon_Help.png"))
        self.ventanaRioBravo.btnMinimizar.setIcon(QIcon(":/Source/Icon_Minimize.png"))
        self.ventanaRioBravo.btnCerrar.setIcon(QIcon(":/Source/Icon_Close.png"))
        self.ventanaRioBravo.lblLogoKWRB.setPixmap(QPixmap(":/Source/LOGO_KWRB.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        
        # Creamos el hilo
        self.Hilo = trabajohilo()
        self.ventanaRioBravo.btnEliminar.clicked.connect(self.RemoveProcessed)
        self.ventanaRioBravo.btnSubir.clicked.connect(self.Cargar)
        self.ventanaRioBravo.btnComenzar.clicked.connect(self.inicialHilo)
        self.ventanaRioBravo.btnAyuda.clicked.connect(self.Ayuda)
        self.ventanaRioBravo.btnMinimizar.clicked.connect(self.minimizar)
        self.ventanaRioBravo.btnCerrar.clicked.connect(self.Cerrar)
        self.ventanaRioBravo.btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.ventanaRioBravo.btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.ventanaRioBravo.btn_Procesados.clicked.connect(self.abrir_ruta_procesados)

        # MENU DE OPCIONES
        self.ventanaRioBravo.actionObjetivos_Mensuales.triggered.connect(self.ObjetivosPagoClientes)
        self.ventanaRioBravo.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)
        #--------------------
        # Señales del hilo
        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)

        Home_DateMovement()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def ObjetivosPagoClientes(self):
        self.ventana_obj = ClassPrincipalObjPagos()
        self.ventana_obj.show()
        
    def FechaMovimiento(self):
        self.ventana_obj = Home_DateMovement()
        self.ventana_obj.show()

#-------------------------------------------------------
    def inicialHilo(self):
        if self.Hilo.isRunning():
            self.Hilo.requestInterruption()
        else:
            self.Hilo.start()
#-----------------------------------------------------

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
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', Variables().ruta_exitosos, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                print("Error al abrir el archivo con Excel:", e)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def mensajeTrabajoTerminado(self):
        msgE = QMessageBox()
        msgE.setWindowTitle("CONTENIDO DE TRABAJOS")
        msgE.setText("La carpeta de trabajo se encuentra totalmente vacia.")
        msgE.setIcon(QMessageBox.Information)
        msgE.setStandardButtons(QMessageBox.Yes)
        msgE.button(QMessageBox.Yes).setText("Entendido")
        x = msgE.exec_()
        if (x == QMessageBox.Yes):
            textoVacio =""
            self.nombreArchivoTrabajando(textoVacio)
#-------------------------------------------------

    def mensajeArchivoErroneo(self, mensaje):
        msgE = QMessageBox()
        msgE.setWindowTitle("TRABAJOS ERRONEOS")
        msgE.setText(f'Los documentos que no se lograron procesar son:\n{mensaje}\nPuedes corregir su nombre y volverlos a subir.\nLa ruta de los errores es:\n {Variables().ruta_error}')
        msgE.setIcon(QMessageBox.Information)
        msgE.setStandardButtons(QMessageBox.Yes)
        msgE.button(QMessageBox.Yes).setText("Entendido")
        x = msgE.exec_()

#--------------------------------------------
# MOSTRAR NOMBRE DEL DOCUMENTO QUE SE ESTA TRABAJANDO
    def nombreArchivoTrabajando(self, nombre):
        if (nombre != ""):
            self.ventanaRioBravo.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.ventanaRioBravo.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.ventanaRioBravo.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.ventanaRioBravo.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
# EVENTOS DEL MOUSE
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

#-----------------------------------------------------
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

# -------------------------------------------------
# CREAR CARPETAS DE TRABAJO
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
            elif not os.path.isdir(f'{Variables().ruta_documentos}'):
                os.makedirs(f'{Variables().ruta_documentos}')
            else:
                pass
#-------------------------------------------------


# MINIMIZAR LA PANTALLA
    def minimizar(self):
        self.showMinimized()
#-------------------------------------------------


# CERRAR LA PANTALLA
    def Cerrar(self):
        self.close()
#--------------------------------------------------


# AGREGAR ARCHIVOS A LA CARPETA DE TRABAJO
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
# ---------------------------------------


# eliminamos los trabajos realizados de la carpeta de exitosos.
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(Variables().ruta_procesados)
        if (len(ruta_trabajos_procesados) == 0):
            mensaje = QMessageBox()
            mensaje.setWindowTitle("HISTORIAL DE REPORTES")
            mensaje.setText("No cuentas con trabajos procesados")
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.button(QMessageBox.Ok).setText("ENTENDIDO")
            x = mensaje.exec_()
        else:
            mensaje = QMessageBox()
            mensaje.setWindowTitle("ELIMINAR REPORTES")
            mensaje.setText("¿Quieres eliminar todos los reportes que ya fueron procesados?")
            mensaje.setIcon(QMessageBox.Question)
            mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mensaje.button(QMessageBox.Yes).setText("ELIMINAR")
            mensaje.button(QMessageBox.No).setText("CANCELAR")
            x = mensaje.exec_()
            if (x == QMessageBox.Yes):
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
                self.Show_Data_Procesado()
                mensaje = QMessageBox()
                mensaje.setWindowTitle("ELIMINACION LISTA")
                mensaje.setText("Todos los archivos fueron removidos")
                mensaje.setIcon(QMessageBox.Information)
                mensaje.setStandardButtons(QMessageBox.Ok)
                mensaje.button(QMessageBox.Ok).setText("ENTENDIDO")
                x = mensaje.exec_()
            else:
                pass
            self.Show_Data_Trabajos()
            self.Show_Data_Procesado()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#-------------------------------------------------------


# APARTADO DE AYUDA
    def Ayuda(self):
        msgA = QMessageBox()
        msgA.setWindowTitle("Información de Ayuda")
        msgA.setText('Para recibir ayuda sobre el funcionamiento del sistema o alguna aclaración, favor de contactar al desarrollador propietario del sistema:\n \nDesarrollador: Luis Ángel Vallejo Pérez\n\nCorreo: angelvallejop9610@gmail.com \n\nTelefono: 271-707-1259 \n \nSí quieres ver los nombres que deben de llevar los documentos, selecciona el boton de "Ver Ayuda"')
        msgA.setIcon(QMessageBox.Information)
        msgA.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msgA.button(QMessageBox.Cancel).setText("Entendido")
        msgA.button(QMessageBox.Ok).setText("Ver Ayuda")
        x = msgA.exec_()
        if (x == QMessageBox.Ok):
            open_new(Variables().pdf)
        else:
            pass
#-------------------------------------------------------
# mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(Variables().ruta_Trabajo)
        self.ventanaRioBravo.TWCola.setRowCount(len(archivos_para_mostrar))
        self.ventanaRioBravo.TWCola.setColumnCount(1)
        self.ventanaRioBravo.TWCola.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ventanaRioBravo.TWCola.setItem(fila, 0, elemento)
        header = self.ventanaRioBravo.TWCola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)



    def Show_Data_Procesado(self):
            archivos_para_mostrar = os.listdir(Variables().ruta_procesados)
            self.ventanaRioBravo.TWProcesado.setRowCount(len(archivos_para_mostrar))
            self.ventanaRioBravo.TWProcesado.setColumnCount(1)
            self.ventanaRioBravo.TWProcesado.setHorizontalHeaderLabels(["Nombre del archivo"])
            for fila, archivo in enumerate(archivos_para_mostrar):
                elemento = QTableWidgetItem(archivo)
                elemento.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Bloqueamos la edición
                elemento.setForeground(QtGui.QColor(0, 0, 0))
                self.ventanaRioBravo.TWProcesado.setItem(fila, 0, elemento)
            header = self.ventanaRioBravo.TWProcesado.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
#--------------------------------------------------


# # LIMPIAR LAS LISTAS
#     def limpiarlista(self):
#         self.ventanaRioBravo.listaTrabajo.clear()
#         self.ventanaRioBravo.listaRealizado.clear()
#-------------------------------------------------


# CLASE DEL HILO----------------------
class trabajohilo(QThread, Variables):
# agregamos una variable de tipo señal
    signal = pyqtSignal()
    signalDocumentosErroneos = pyqtSignal(str)
    signalShowTrabajos = pyqtSignal()
    signalShowProcesados = pyqtSignal()
    signalNombreArchivo =  pyqtSignal(str)


# COMENZAR EL PROCESO DE TRABAJO.
    # HILO DEL TRABAJO DE "RIO BRAVO"  
    def run(self):
        array_errores = []
        #---------------------------------------
        # diccionario de los archivos.
        diccionario_archivos = {
            "SVR.xlsx" : KenworthConnect().SalidasEnVale,
            "RR.xlsx" : KenworthConnect().Refacciones,
            "OSR.xlsx" : KenworthConnect().OrdenesDeServicio,
            "SDR.xlsx" : KenworthConnect().ServicioDetallado,
            "BOR.xlsx" : KenworthConnect().BackOrder,
            "CDR.xlsx" : KenworthConnect().ComprasDetallado,
            "CR.xlsx" : KenworthConnect().Credito,
            "TER.xlsx" : KenworthConnect().TrabajosPorEstado,
            "PCR.xlsx" : KenworthConnect().PagosClientes,
            "ICR.xlsx" :KenworthConnect().InventarioCosteado,
            "IUR.xlsx" : KenworthConnect().InventarioDeUnidades,
            "RFR.xlsx" : KenworthConnect().ResultadosFinancieros,
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
                        except:
                            pass
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
    window = KenworthRioBravo()
    window.show()
    sys.exit(app.exec_())