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
from Clases.Home_rutas import *
from datetime import *
import webbrowser

class my_app(QMainWindow, Variables):
    def __init__(self): 
        super(my_app, self).__init__()
        self.ui = Ui_VPrincipal()
        self.ui.setupUi(self)
        self.setWindowTitle("Menu de Sucursales")
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/LOGO_KREI.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btc_btc_rutas.setIcon(QIcon("Source/rutas.svg"))
        self.ui.btn_btn_kwrb.clicked.connect(self.VentanaRioBravo)
        self.ui.btn_btn_kweste.clicked.connect(self.VentanaKWESTE)
        self.ui.btn_btn_kwkrei.clicked.connect(self.VentanaKREI)
        self.ui.btn_btn_kwsonora.clicked.connect(self.VentanaSonora)
        self.ui.btc_btc_rutas.clicked.connect(self.rutas)

#-------------------------------------------------
    def VentanaRioBravo(self):
        self.Ventana = Home_KWRB()
        self.Ventana.show() 
#-------------------------------------------------
    def VentanaKWESTE(self):
        self.Ventana = Home_KWESTE()
        self.Ventana.show()
#-------------------------------------------------
    def VentanaKREI(self):
        self.Ventana = Home_KREI()
        self.Ventana.show() 
#-------------------------------------------------
    def VentanaSonora(self):
        self.Ventana = Home_KenworthSonora()
        self.Ventana.show() 
#-------------------------------------------------
    def rutas(self):
        self.rutas = rutas()
        self.rutas.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = my_app()
    window.show()
    sys.exit(app.exec_())