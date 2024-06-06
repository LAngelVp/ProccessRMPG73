#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF
from ..globalModulesShare.resources import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from webbrowser import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.Inicio_FechaMovimiento import *
from .KenworthConnect import *
from ..globalModulesShare.InicialClassObjetivos import *
from ..ventanaspy.V_KWRB import *
from ..globalModulesShare.Home_rutas import *
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas
import subprocess
class Home_KWRB(QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(Home_KWRB, self).__init__()
        self.ventanaRioBravo = Ui_Kenworth_Rio_Bravo()
        self.ventanaRioBravo.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ventanaRioBravo.btn_btn_Ayuda.setIcon(QIcon(":/Source/Icon_Help.png"))
        self.ventanaRioBravo.btc_btc_Minimizar.setIcon(QIcon(":/Source/Icon_Minimize.png"))
        self.ventanaRioBravo.btc_btc_Cerrar.setIcon(QIcon(":/Source/Icon_Close.png"))
        self.ventanaRioBravo.lblLogoKWRB.setPixmap(QPixmap(":/Source/LOGO_KWRB.png"))
        Icon_Delete = QIcon(":/Source/Icon_Delete.png")
        Icon_Proccess = QIcon(":/Source/Icon_Proccess.png")
        Icon_Upload = QIcon(":/Source/Icon_Upload.png")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
       
        
        self.variables = Variables()
        
        # Creamos el hilo
        self.Hilo = trabajohilo()

        self.ventanaRioBravo.btn_btn_Eliminar.setIcon(Icon_Delete)
        self.ventanaRioBravo.btn_btn_Eliminar.setIconSize(QtCore.QSize(24, 24))
        self.ventanaRioBravo.btn_btn_Comenzar.setIcon(Icon_Proccess)
        self.ventanaRioBravo.btn_btn_Comenzar.setIconSize(QtCore.QSize(24, 24))
        self.ventanaRioBravo.btn_btn_Subir.setIcon(Icon_Upload)
        self.ventanaRioBravo.btn_btn_Subir.setIconSize(QtCore.QSize(24, 24))


        self.ventanaRioBravo.btn_btn_Eliminar.clicked.connect(self.RemoveProcessed)
        self.ventanaRioBravo.btn_btn_Subir.clicked.connect(self.Cargar)
        self.ventanaRioBravo.btn_btn_Comenzar.clicked.connect(self.inicialHilo)
        self.ventanaRioBravo.btn_btn_Ayuda.clicked.connect(self.Ayuda)
        self.ventanaRioBravo.btc_btc_Minimizar.clicked.connect(self.minimizar)
        self.ventanaRioBravo.btc_btc_Cerrar.clicked.connect(self.Cerrar)
        self.ventanaRioBravo.btn_btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.ventanaRioBravo.btn_btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.ventanaRioBravo.btn_btn_Procesados.clicked.connect(self.abrir_ruta_procesados)

        # MENU DE OPCIONES
        self.ventanaRioBravo.actionObjetivos_Mensuales_PagosClientes.triggered.connect(self.ObjetivosPagoClientes)
        self.ventanaRioBravo.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)
        self.ventanaRioBravo.actionDirecciones_de_envio.triggered.connect(self.direcciones_envio)
        #--------------------
        # Señales del hilo
        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)

        # if not os.path.exists(self.variables.route_kwrb):
        #     os.mkdir(self.variables.route_kwrb)
        # else:
        #     pass
        
        self.Creacion_Carpetas()

        
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    # -------------------------------------------------
# CREAR CARPETAS DE TRABAJO
    def Creacion_Carpetas(self):
        # Rutas de las carpetas que se deben verificar/crear
        rutas_a_verificar = [
            self.variables.ruta_Trabajos_kwrb,
            self.variables.ruta_original_kwrb,
            self.variables.ruta_errores_kwrb,
            self.variables.ruta_exitosos_kwrb
        ]
        
        # Verificar si todas las carpetas ya existen
        todas_existen = all(os.path.exists(ruta) for ruta in rutas_a_verificar)
        
        if todas_existen:
            print("Todas las carpetas necesarias ya existen, no se realizará ninguna acción.")
        else:
            # Crear las carpetas que no existan
            for ruta in rutas_a_verificar:
                if not os.path.exists(ruta):
                    os.makedirs(ruta, exist_ok=True)
            print("Las carpetas necesarias han sido creadas.")
#-------------------------------------------------
    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()

    def ObjetivosPagoClientes(self):
        self.ventana_obj = ClassPrincipalObjPagos()
        self.ventana_obj.show()
        
    def FechaMovimiento(self):
        self.ventana_obj = Home_DateMovement()
        self.ventana_obj.show()

    def direcciones_envio(self):
        self.ventana_rutas = rutas()
        self.ventana_rutas.show()
#-------------------------------------------------------
    def inicialHilo(self):
        if self.Hilo.isRunning():
            self.Hilo.requestInterruption()
        else:
            self.Hilo.start()
#-----------------------------------------------------

    def abrir_ruta_errores(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_errores_kwrb, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_originales(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_original_kwrb, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_procesados(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_exitosos_kwrb, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def mensajeTrabajoTerminado(self):
        Mensajes_Alertas(
            "Trabajos Terminados",
            "Todos los trabajos que se comenzaron fueron insertados por el proceso lógico del sistema.",
            QMessageBox.Icon.Information,
            None,
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        textoVacio =""
        self.nombreArchivoTrabajando(textoVacio)
#-------------------------------------------------

    def mensajeArchivoErroneo(self, mensaje):
        Mensajes_Alertas(
            "Errores durante el proceso",
            f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {self.variables.ruta_errores_kwrb}',
            QMessageBox.Icon.Critical,
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
            self.ventanaRioBravo.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.ventanaRioBravo.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.ventanaRioBravo.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.ventanaRioBravo.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
# EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())



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
        ubicacion_carga = os.chdir(self.variables.root_directory_system)
        options = QFileDialog().options()
        # options |= QFileDialog.DontUseNativeDialog  # Evitar el uso del diálogo nativo del sistema operativo (opcional)
        options |= QFileDialog.Option.ReadOnly  # Permite abrir los archivos solo en modo lectura (opcional)
        options |= QFileDialog.Option.HideNameFilterDetails  # Ocultar detalles del filtro (opcional)
        options |= QFileDialog.Option.DontResolveSymlinks  # No resolver enlaces simbólicos (opcional)

        selected_filter = "Hojas de Excel (*.xlsx);;Todos los archivos (*)"
        
        if os.path.isdir(self.variables.ruta_Trabajos_kwrb) == True:
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwrb)
            except:
                pass
        else:
            os.makedirs(self.variables.ruta_Trabajos_kwrb)
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwrb)
            except:
                pass
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
# ---------------------------------------
    def eliminar(self):
        carpeta_contenido_eliminar = os.listdir(self.variables.ruta_exitosos_kwrb)
        for archivo in carpeta_contenido_eliminar:
            if (len(carpeta_contenido_eliminar) != 0):
                try:
                    archivo_completo = os.path.join(self.variables.ruta_exitosos_kwrb, archivo)
                    os.remove(archivo_completo)
                except:
                    pass
            else:
                pass

# eliminamos los trabajos realizados de la carpeta de exitosos.
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(self.variables.ruta_exitosos_kwrb)
        if (len(ruta_trabajos_procesados) == 0):
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.Aceptar_callback)]).Eliminar_vacio
        else:
            Mensajes_Alertas(None,None,None,None,botones=[("Eliminar", self.eliminar)]).Eliminar_lleno
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#-------------------------------------------------------
    def Ayuda(self):
        self.Mensaje_Ayuda = Mensajes_Alertas(
            "Información de Ayuda",
            'Si tienes problemas con la aplicación debido a que no sabes como guardar tus archivos de excel para que puedan ser transformados.\nPuedes ver el manual de usuario dando click en el boton de "Ver"',
            QMessageBox.Icon.Information,  # Aquí se pasa el tipo de ícono
            None,
            botones = [
                ("Aceptar", self.Aceptar_callback),
                ("Ver", self.Ayuda_callback)
            ]
        ).Apartado_Ayuda

    def Aceptar_callback(self):
        pass
    def Ayuda_callback(self):
        open_new(self.variables.pdf)
#-------------------------------------------------------
# mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_Trabajos_kwrb)
        self.ventanaRioBravo.Tabla_Cola.setRowCount(len(archivos_para_mostrar))
        self.ventanaRioBravo.Tabla_Cola.setColumnCount(1)
        self.ventanaRioBravo.Tabla_Cola.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ventanaRioBravo.Tabla_Cola.setItem(fila, 0, elemento)
        header = self.ventanaRioBravo.Tabla_Cola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)



    def Show_Data_Procesado(self):
            archivos_para_mostrar = os.listdir(self.variables.ruta_exitosos_kwrb)
            self.ventanaRioBravo.Tabla_Procesados.setRowCount(len(archivos_para_mostrar))
            self.ventanaRioBravo.Tabla_Procesados.setColumnCount(1)
            self.ventanaRioBravo.Tabla_Procesados.setHorizontalHeaderLabels(["Nombre del archivo"])
            for fila, archivo in enumerate(archivos_para_mostrar):
                elemento = QTableWidgetItem(archivo)
                elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
                elemento.setForeground(QtGui.QColor(0, 0, 0))
                self.ventanaRioBravo.Tabla_Procesados.setItem(fila, 0, elemento)
            header = self.ventanaRioBravo.Tabla_Procesados.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
#--------------------------------------------------


# # LIMPIAR LAS LISTAS
#     def limpiarlista(self):
#         self.ventanaRioBravo.listaTrabajo.clear()
#         self.ventanaRioBravo.listaRealizado.clear()
#-------------------------------------------------


# CLASE DEL HILO----------------------
class trabajohilo(QThread):
# agregamos una variable de tipo señal
    signal = pyqtSignal()
    signalDocumentosErroneos = pyqtSignal(str)
    signalShowTrabajos = pyqtSignal()
    signalShowProcesados = pyqtSignal()
    signalNombreArchivo =  pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.variables = Variables()


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
            carpeta_de_trabajos = os.listdir(self.variables.ruta_Trabajos_kwrb)
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
                        array_errores.append(nombre_archivo)
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
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwrb, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_original_kwrb, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_original_kwrb)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_original_kwrb)
#--------------------------------------------------

    
# COMPRROBAR SI EXISTE EL DOCUMENTO ERRONEO EN EL DESTINO
    def Comprobacion_Errores(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwrb, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_errores_kwrb, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_errores_kwrb)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_errores_kwrb)
#--------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Home_KWRB()
    window.show()
    sys.exit(app.exec_())