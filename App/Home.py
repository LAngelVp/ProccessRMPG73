#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
from resources import *
from PyQt5 import  *
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from VPrincipal import *
# comment importamos concesionarios
from Reports_Logic.Rio_Bravo.Home_KWRB import *
from Reports_Logic.KenworthEste.Home_KWESTE import *
from Reports_Logic.KREI.Home_KREI import *
from Reports_Logic.Kenworth_Sonora.Home_KWSonora import *
#------------
from datetime import *
import webbrowser

class my_app(QMainWindow, Variables):
    def __init__(self):
        super(my_app, self).__init__()
        
        self.ui = Ui_VPrincipal()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Menu de Sucursales")
        # self.ui.centralwidget.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/LOGO_KREI.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btc_btc_cerrar.setIcon(QIcon(":Source/Icon_Close.png"))
        self.ui.btc_btc_minimizar.setIcon(QIcon(":Source/Icon_Minimize.png"))
        self.ui.panel_encabezado.setStyleSheet("margin-top:5px;")

        self.ventanas_abiertas = {}
        # self.ui.btn_btn_kwrb.clicked.connect(self.VentanaRioBravo)
        # self.ui.btn_btn_kweste.clicked.connect(self.VentanaKWESTE)
        # self.ui.btn_btn_kwkrei.clicked.connect(self.VentanaKREI)
        # self.ui.btn_btn_kwsonora.clicked.connect(self.VentanaSonora)
        
        self.ui.btn_btn_kwrb.clicked.connect(lambda: self.abrir_ventana("Rio Bravo", Home_KWRB))
        self.ui.btn_btn_kweste.clicked.connect(lambda: self.abrir_ventana("Kenworth del Este", Home_KWESTE))
        self.ui.btn_btn_kwkrei.clicked.connect(lambda: self.abrir_ventana("KREI", Home_KREI))
        self.ui.btn_btn_kwsonora.clicked.connect(lambda: self.abrir_ventana("Kenworth Sonora", Home_KenworthSonora))


        self.ui.btc_btc_cerrar.clicked.connect(self.cerrar)
        self.ui.btc_btc_minimizar.clicked.connect(self.minimizar)

    def abrir_ventana(self, titulo, clase_ventana):
        if clase_ventana.__name__ not in self.ventanas_abiertas:
            ventana = clase_ventana()
            ventana.setWindowTitle(titulo)
            ventana.show()
            self.ventanas_abiertas[clase_ventana.__name__] = ventana
            ventana.closed.connect(lambda: self.ventanas_abiertas.pop(clase_ventana.__name__))

        else:
            QMessageBox.warning(self, "Advertencia", f"Ya hay una ventana de {titulo} abierta.")

# #-------------------------------------------------
#     def VentanaRioBravo(self):
#         self.Ventana = Home_KWRB()
#         self.Ventana.show() 
# #-------------------------------------------------
#     def VentanaKWESTE(self):
#         self.Ventana = Home_KWESTE()
#         self.Ventana.show()
# #-------------------------------------------------
#     def VentanaKREI(self):
#         self.Ventana = Home_KREI()
#         self.Ventana.show() 
# #-------------------------------------------------
#     def VentanaSonora(self):
#         self.Ventana = Home_KenworthSonora()
#         self.Ventana.show() 
#-------------------------------------------------
    def cerrar(self):
        self.close()

    def minimizar(self):
        self.showMinimized()

    # EVENTOS DEL MOUSE
    def mousePressEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton:
                self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
        except:
            pass
#-----------------------------------------------------
    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            if event.buttons() == Qt.LeftButton:
                self.move(event.globalPos() - self.drag_start_position)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = my_app()
    window.show()
    sys.exit(app.exec_())