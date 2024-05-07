import os
import sys
from ..globalModulesShare.resources import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from ..ventanaspy.fecha import *
from .Creacion_JSON_FechaMovimiento import *
from .Logica_Reportes.Variables.ContenedorVariables import Variables

class Home_DateMovement(QWidget, Variables):
    def __init__(self):
        super(Home_DateMovement,self).__init__()
        self.ui = Ui_Form_FechaMovimiento()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        

        # comment Colocamos la fecha actual a la caja de Fecha
        self.current_date = QDate.currentDate()
        self.ui.date_edit_date_movement.setDate(self.current_date)

        #comment connect event, date select
        self.ui.date_edit_date_movement.dateChanged.connect(self.update_json)

        current_date = self.ui.date_edit_date_movement.date().toString("dd/MM/yyyy")
        CreateJson().update_date(current_date)


    def update_json(self):
        # Obtener la fecha del QDateEdit y convertirla a una cadena con el formato deseado
        current_date = self.ui.date_edit_date_movement.date().toString("dd/MM/yyyy")
        CreateJson(Variables().route_file_date_movement).update_date(current_date)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Home_DateMovement()
    ventana.show()
    sys.exit(app.exec_())
