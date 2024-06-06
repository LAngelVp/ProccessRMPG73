#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ 
#########################
import sys
import os
from .globalModulesShare.resources import *
from .globalModulesShare.icono import *
from PyQt6 import  *
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QPixmap
# comment importamos concesionarios
from .Rio_Bravo.Home_KWRB import *
from .KenworthEste.Home_KWESTE import *
from .KREI.Home_KREI import *
from .Kenworth_Sonora.Home_KWSonora import *
#-----------
from .globalModulesShare.ContenedorVariables import Variables
from .ventanaspy.VPrincipal import Ui_VPrincipal 
from Front.inicio_sesion import UI_Inicio_Sesion

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
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/DevRous2.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btc_btc_cerrar.setIcon(QIcon(":Source/Icon_Close.png"))
        self.ui.btc_btc_minimizar.setIcon(QIcon(":Source/Icon_Minimize.png")) 
        self.ui.panel_encabezado.setStyleSheet("margin-top:5px;")
        
        self.ui.btn_btn_kwrb.clicked.connect(self.abrirkwrb)
        self.ui.btn_btn_kweste.clicked.connect(self.abrirkweste)
        self.ui.btn_btn_kwkrei.clicked.connect(self.abrirkwkrei)
        self.ui.btn_btn_kwsonora.clicked.connect(self.abrirkwsonora)
        self.ui.btc_btc_cerrar.clicked.connect(self.cerrar)
        self.ui.btc_btc_minimizar.clicked.connect(self.minimizar)

        if not os.path.exists(Variables().help_directory):
            os.makedirs(Variables().help_directory, exist_ok=True)
        else:
            pass

    
    def cerrar(self):
        self.close()

    def abrirkwrb(self):
        self.ventana = Home_KWRB()
        self.ventana.show()
    def abrirkwkrei(self):
        self.ventana = Home_KREI()
        self.ventana.show()
    def abrirkweste(self):
        self.ventana = Home_KWESTE()
        self.ventana.show()
    def abrirkwsonora(self):
        self.ventana = Home_KenworthSonora()
        self.ventana.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = PrincipalWindow()
    ventana_principal.show()
    sys.exit(app.exec())
