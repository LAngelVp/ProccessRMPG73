#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ 
#########################
import sys
import os
from Reports_Logic.globalModulesShare.resources import *
from PyQt6 import  *
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QPixmap
# comment importamos concesionarios
from Reports_Logic.Rio_Bravo.Home_KWRB import *
from Reports_Logic.KenworthEste.Home_KWESTE import *
from Reports_Logic.KREI.Home_KREI import *
from Reports_Logic.Kenworth_Sonora.Home_KWSonora import *
#------------
from Reports_Logic.globalModulesShare.ContenedorVariables import Variables
from Reports_Logic.ventanaspy.VPrincipal import Ui_VPrincipal 
class PrincipalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.ui = Ui_VPrincipal()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("Menu de Sucursales")
        # self.ui.centralwidget.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/LOGO_KREI.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btc_btc_cerrar.setIcon(QIcon(":Source/Icon_Close.png"))
        self.ui.btc_btc_minimizar.setIcon(QIcon(":Source/Icon_Minimize.png"))
        self.ui.panel_encabezado.setStyleSheet("margin-top:5px;")

        self.ventanas_abiertas = {}
        
        self.ui.btn_btn_kwrb.clicked.connect(lambda: self.abrir_ventana("Rio Bravo", Home_KWRB))
        self.ui.btn_btn_kweste.clicked.connect(lambda: self.abrir_ventana("Kenworth del Este", Home_KWESTE))
        self.ui.btn_btn_kwkrei.clicked.connect(lambda: self.abrir_ventana("KREI", Home_KREI))
        self.ui.btn_btn_kwsonora.clicked.connect(lambda: self.abrir_ventana("Kenworth Sonora", Home_KenworthSonora))


        self.ui.btc_btc_cerrar.clicked.connect(self.cerrar)
        self.ui.btc_btc_minimizar.clicked.connect(self.minimizar)

        self.createProjectDirectory()

    def abrir_ventana(self, titulo, clase_ventana):
        if clase_ventana.__name__ not in self.ventanas_abiertas:
            ventana = clase_ventana()
            ventana.setWindowTitle(titulo)
            ventana.show()
            self.ventanas_abiertas[clase_ventana.__name__] = ventana
            ventana.closed.connect(lambda: self.ventanas_abiertas.pop(clase_ventana.__name__))

        else:
            QMessageBox.warning(self, "Advertencia", f"Ya hay una ventana de {titulo} abierta.")

    def createProjectDirectory(self):
        if not os.path.exists(self.variables.global_route_project):
            os.mkdir(self.variables.global_route_project)
        else:
            if not os.path.exists(self.variables.help_directory):
                os.mkdir(self.variables.help_directory)
            else:
                pass


    def cerrar(self):
        self.close()

    def minimizar(self):
        self.showMinimized()

    # EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())


def main():
    app = QApplication(sys.argv)
    ventana_principal = PrincipalWindow()
    ventana_principal.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()