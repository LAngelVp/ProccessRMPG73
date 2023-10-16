import sys
from resources import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from .UI.V_KWSonora import *
from webbrowser import *
from .Logica_Reportes.Variables.ContenedorVariables import Variables
class Home_KenworthSonora(QMainWindow):
    def __init__(self):
        super(Home_KenworthSonora,self).__init__()
        self.ui = Ui_MainWindowKenworthSonora()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) # comment_line quitamos la barra superior
        #comment apartado de ligas de los iconos
        self.ui.btnAyuda.setIcon(QIcon(":/Source/Icon_Help.png"))
        self.ui.btnMinimizar.setIcon(QIcon(":/Source/Icon_Minimize.png"))
        self.ui.btnCerrar.setIcon(QIcon(":/Source/Icon_Close.png"))
        self.ui.lblLogoKWS.setPixmap(QPixmap(":/Source/Logo_KWSonora.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        # comment conexiones de los botones
        self.ui.btnAyuda.clicked.connect(self.Help)
        self.ui.btnCerrar.clicked.connect(self.Cerrar)
        self.ui.btnMinimizar.clicked.connect(self.Minimizar)



    def Help(self):
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
     # cerrar la ventana
    def Cerrar(self):
        self.close()
    # minimizar la ventana
    def Minimizar(self):
        self.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Home_KenworthSonora()
    ventana.show()
    sys.exit(app.exec_())