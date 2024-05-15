import sys
import os
import shutil
from ..globalModulesShare.resources import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from ..ventanaspy.V_KWSonora import *
from ..globalModulesShare.InicialClassObjetivos import *
from ..globalModulesShare.Inicio_FechaMovimiento import *
from webbrowser import *
import subprocess
from ..globalModulesShare.ContenedorVariables import Variables
from .Kenworth_Connect import *
from ..globalModulesShare.Home_rutas import *
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas

class Home_KenworthSonora(QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(Home_KenworthSonora,self).__init__()
        self.ui = Ui_Kenworth_Sonora()
        self.ui.setupUi(self)

        self.variables = Variables()

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint) # comment_line quitamos la barra superior
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # comment llamamos el metodo de creacion de carpetas
        self.Creacion_Carpetas()
        # comment variables a las rutas de los iconos e imagenes
        Icon_Cerrar = QIcon(":/Source/Icon_Close.png")
        Icon_Minimizar = QIcon(":/Source/Icon_Minimize.png")
        Icon_Help = QIcon(":/Source/Icon_Help.png")
        Icon_Delete = QIcon(":/Source/Icon_Delete.png")
        Icon_Proccess = QIcon(":/Source/Icon_Proccess.png")
        Icon_Upload = QIcon(":/Source/Icon_Upload.png")
        logo = QPixmap(":/Source/Logo_KWSonora.png")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
    
        # comment colocar los iconos e imagenes en su correspondiente elemento.
        self.ui.lblLogoKWS.setPixmap(logo)
        self.ui.btc_btc_Cerrar.setIcon(Icon_Cerrar)
        self.ui.btc_btc_Minimizar.setIcon(Icon_Minimizar)
        self.ui.btn_btn_Ayuda.setIcon(Icon_Help)
        self.ui.btn_btn_Eliminar.setIcon(Icon_Delete)
        self.ui.btn_btn_Eliminar.setIconSize(QtCore.QSize(24, 24))
        self.ui.btn_btn_Comenzar.setIcon(Icon_Proccess)
        self.ui.btn_btn_Comenzar.setIconSize(QtCore.QSize(24, 24))
        self.ui.btn_btn_Subir.setIcon(Icon_Upload)
        self.ui.btn_btn_Subir.setIconSize(QtCore.QSize(24, 24))
        # creamos el hilo
        self.Hilo = trabajohilo()
        #conexiones de los botones
        self.ui.btn_btn_Subir.clicked.connect(self.Cargar)
        self.ui.btn_btn_Comenzar.clicked.connect(self.ComenzarProceso)
        self.ui.btn_btn_Eliminar.clicked.connect(self.RemoveProcessed)
        self.ui.btn_btn_Ayuda.clicked.connect(self.Ayuda)
        self.ui.btc_btc_Cerrar.clicked.connect(self.Cerrar)
        self.ui.btc_btc_Minimizar.clicked.connect(self.Minimizar)
        self.ui.btn_btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.ui.btn_btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.ui.btn_btn_Procesados.clicked.connect(self.abrir_ruta_procesados)

        # MENU DE OPCIONES
        self.ui.actionObjetivos_Mensuales.triggered.connect(self.ObjetivosPagoClientes)
        self.ui.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)
        self.ui.actionDirecciones_de_envio.triggered.connect(self.direcciones_envio)


        # señales del hilo
        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)

        Home_DateMovement()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()
        


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

        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_errores_kwsonora, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
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
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_original_kwsonora, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
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
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_exitosos_kwsonora, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
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
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#-------------------------------------------------


    def mensajeArchivoErroneo(self, mensaje):
        Mensajes_Alertas(
            "Errores durante el proceso",
            f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {self.variables.ruta_errores_kwsonora}',
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
            self.ui.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.ui.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.ui.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.ui.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
#-------------------------------------------------------
# EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())
    # Apartado de funciones
    #-------------------------
    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_Trabajos_kwsonora)
        self.ui.Tabla_Cola.setRowCount(len(archivos_para_mostrar))
        self.ui.Tabla_Cola.setColumnCount(1)
        self.ui.Tabla_Cola.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ui.Tabla_Cola.setItem(fila, 0, elemento)
        header = self.ui.Tabla_Cola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Procesado(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_exitosos_kwsonora)
        self.ui.Tabla_Procesado.setRowCount(len(archivos_para_mostrar))
        self.ui.Tabla_Procesado.setColumnCount(1)
        self.ui.Tabla_Procesado.setHorizontalHeaderLabels(["Nombre del archivo"])
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QtGui.QColor(0, 0, 0))
            self.ui.Tabla_Procesado.setItem(fila, 0, elemento)
        header = self.ui.Tabla_Procesado.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)


    def Creacion_Carpetas(self):
        directorio = os.listdir(self.variables.global_route_project)
        for i in directorio:
            if not os.path.exists(f'{self.variables.ruta_Trabajos_kwsonora}'):
                os.makedirs(f'{self.variables.ruta_Trabajos_kwsonora}')
            elif not os.path.exists(f'{self.variables.ruta_original_kwsonora}'):
                os.makedirs(f'{self.variables.ruta_original_kwsonora}')
            elif not os.path.isdir(f'{self.variables.ruta_errores_kwsonora}'):
                os.makedirs(f'{self.variables.ruta_errores_kwsonora}')
            elif not os.path.isdir(f'{self.variables.ruta_exitosos_kwsonora}'):
                os.makedirs(f'{self.variables.ruta_exitosos_kwsonora}')
            else:
                break
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
        ubicacion_carga = os.chdir(self.variables.root_directory_system)
        options = QFileDialog().options()
        # options |= QFileDialog.DontUseNativeDialog  # Evitar el uso del diálogo nativo del sistema operativo (opcional)
        options |= QFileDialog.Option.ReadOnly  # Permite abrir los archivos solo en modo lectura (opcional)
        options |= QFileDialog.Option.HideNameFilterDetails  # Ocultar detalles del filtro (opcional)
        options |= QFileDialog.Option.DontResolveSymlinks  # No resolver enlaces simbólicos (opcional)

        selected_filter = "Hojas de Excel (*.xlsx);;Todos los archivos (*)"
        
        if os.path.isdir(self.variables.ruta_Trabajos_kwsonora) == True:
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwsonora)
            except:
                pass
        else:
            os.makedirs(self.variables.ruta_Trabajos_kwsonora)
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwsonora)
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
        carpeta_contenido_eliminar = os.listdir(self.variables.ruta_exitosos_kwsonora)
        for archivo in carpeta_contenido_eliminar:
            if (len(carpeta_contenido_eliminar) != 0):
                try:
                    archivo_completo = os.path.join(self.variables.ruta_exitosos_kwsonora, archivo)
                    os.remove(archivo_completo)
                except:
                    pass
            else:
                pass
    # eliminamos los trabajos realizados de la carpeta de exitosos.
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(self.variables.ruta_exitosos_kwsonora)
        if (len(ruta_trabajos_procesados) == 0):
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.Aceptar_callback)]).Eliminar_vacio
        else:
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.eliminar)]).Eliminar_lleno
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    # mostramos el apartado de ayuda
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
            "CS.xlsx" : KenworthConnect().Credito,
            "SVS.xlsx" : KenworthConnect().SalidaEnVale,
            "RS.xlsx" : KenworthConnect().Refacciones,
            "PCS.xlsx" : KenworthConnect().PagoDeClientes,
            "ICS.xlsx" : KenworthConnect().InventarioCosteadoAndInventarioPorDia,
            "OSS.xlsx" : KenworthConnect().OrdenesDeServicio,
            "TES.xlsx" : KenworthConnect().TrabajosPorEstado,
            "IUS.xlsx" : KenworthConnect().InventarioDeUnidades,
            "RFS.xlsx" : KenworthConnect().ResultadosFinancieros,
            "CDS.xlsx" : KenworthConnect().Compras,
            "BOS.xlsx" : KenworthConnect().BackOrder,
            "SDS.xlsx" : KenworthConnect().ServicioDetallado,
            "VSS.xlsx" : KenworthConnect().VentasServicio
        }
        #-----------------------------------------------
        while True:
            carpeta_de_trabajos = os.listdir(self.variables.ruta_Trabajos_kwsonora)
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
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwsonora, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_original_kwsonora, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_original_kwsonora)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_original_kwsonora)
#--------------------------------------------------
#--------------------------------------------------
# COMPRROBAR SI EXISTE EL DOCUMENTO ERRONEO EN EL DESTINO
    def Comprobacion_Errores(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwsonora, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_errores_kwsonora, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_errores_kwsonora)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_errores_kwsonora)
#--------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Home_KenworthSonora()
    ventana.show()
    sys.exit(app.exec_())