#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5 import *
from resources import *
from Logica_Reportes.Variables.ContenedorVariables import Variables
from UI.IU_VENDEDORES import *

class Vendedores(QWidget, Variables):
    def __init__(self):
        super(Vendedores,self).__init__()
        self.ui = Ui_Formulario_Vendedores()
        self.ui.setupUi(self)
        self.ui.Vendedores_Refacciones.setCurrentIndex(0)
        self.setWindowTitle("Clasificación de Vendedores")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.tabla_vendedoresrefacciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabla_vendedoresrefacciones_servicio.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Configura el modo de ajuste de tamaño para todas las columnas
        
        # self.ui.tabla_vendedoresrefacciones.resizeColumnsToContents()
        # try:
        #     self.json_vendedores_refacciones = Variables().clasificacion_vendedores_departamentos_refacciones()
        #     print(self.json_vendedores_refacciones)
        # except FileNotFoundError as e:
        #     pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Vendedores()
    window.show()
    sys.exit(app.exec_())