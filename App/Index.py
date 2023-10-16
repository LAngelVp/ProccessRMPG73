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
from Reports_Logic.Rio_Bravo.index_KWRioBravo import *
from Reports_Logic.KenworthEste.indexKWESTE import *
from Reports_Logic.KREI.indexKREI import *
from Reports_Logic.Kenworth_Sonora.Home_Kenworth_Sonora import *
#------------
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
        self.ui.btnKWRB.clicked.connect(self.VentanaRioBravo)
        self.ui.btnKWESTE.clicked.connect(self.VentanaKWESTE)
        self.ui.btnKWKREI.clicked.connect(self.VentanaKREI)
        self.ui.btnKWS.clicked.connect(self.VentanaSonora)

#-------------------------------------------------
    def VentanaRioBravo(self):
        self.VentanaKWRioBravo = KenworthRioBravo()
        self.VentanaKWRioBravo.show() 
#-------------------------------------------------
    def VentanaKWESTE(self):
        self.ventanaKWESTE = VentanaKWESTE()
        self.ventanaKWESTE.show()
#-------------------------------------------------
    def VentanaKREI(self):
        self.VentanaKWKREI = KenworthKREI()
        self.VentanaKWKREI.show() 
#-------------------------------------------------
    def VentanaSonora(self):
        self.VentanaKWSonora = Home_KenworthSonora()
        self.VentanaKWSonora.show() 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = my_app()
    window.show()
    sys.exit(app.exec_())