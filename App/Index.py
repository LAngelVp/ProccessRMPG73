#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
from resources import *
from PyQt5 import  *
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
#NOTE importamos las ventanas de FRONT-END
from VPrincipal import *
from Reports_Logic.Rio_Bravo.index_KWRioBravo import *
from Reports_Logic.KenworthEste.indexKWESTE import *
from Reports_Logic.KREI.indexKREI import *
#______________________________
from Reports_Logic.Rio_Bravo.KENWORTH_RioBravo import KENWORTH_Rio_Bravo
from datetime import *
import webbrowser
class my_app(QMainWindow, Variables):
# VENTANA PRINCIPAL
    def __init__(self):
        super(my_app, self).__init__()
        self.ui = Ui_VPrincipal()
        self.ui.setupUi(self)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowTitle("Menu de Sucursales")
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/LOGO_KREI.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btnKWRB.clicked.connect(self.VentanaRioBravo)
        self.ui.btnKWESTE.clicked.connect(self.VentanaKWESTE)
        self.ui.btnKWKREI.clicked.connect(self.VentanaKREI)

#-------------------------------------------------
# MOSTRAR LA VENTANA DE KENWORTH RIO BRAVO
    def VentanaRioBravo(self):
        self.VentanaKWRioBravo = KenworthRioBravo()
        self.VentanaKWRioBravo.show() 
#-------------------------------------------------
# MOSTRAR LA VENTANA DE KENWORTH DEL ESTE
    def VentanaKWESTE(self):
        self.ventanaKWESTE = VentanaKWESTE()
        self.ventanaKWESTE.show()
#-------------------------------------------------
# MOSTRAR LA VENTANA DE KREI
    def VentanaKREI(self):
        self.VentanaKWKREI = KenworthKREI()
        self.VentanaKWKREI.show() 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = my_app()
    window.show()
    sys.exit(app.exec_())