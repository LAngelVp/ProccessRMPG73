import os
import sys
from Reports_Logic.globalModulesShare.resources import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
# from ...Front.ventanaspy.V_FECHA_MOVI import *
from ..ventanaspy.fecha import *
from .ContenedorVariables import Variables
from .documentos_json import creacion_json

class Home_DateMovement(QWidget):
    def __init__(self):
        super(Home_DateMovement,self).__init__()
        self.variables = Variables()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.setWindowTitle('Fecha Movimiento')
        

        # comment Colocamos la fecha actual a la caja de Fecha
        fecha = creacion_json(self.variables.help_directory,self.variables.movement_date_document_file).comprobar_existencia
        fecha_obtenida =  fecha[0]['fecha_movimiento']
        self.current_date = QDate.fromString(fecha_obtenida, "yyyy-MM-dd")
        self.ui.date_edit_date_movement.setDate(self.current_date)

        #comment connect event, date select
        self.ui.date_edit_date_movement.dateChanged.connect(self.update_json)



    def update_json(self, nueva_fecha):
        fecha_antigua = creacion_json(self.variables.help_directory,self.variables.movement_date_document_file).comprobar_existencia
        id_fecha = fecha_antigua[0]['id']
        id = {"id" : str(id_fecha)}
        nueva_fecha_tipada = nueva_fecha.toString("yyyy-MM-dd")
        nuevo_objeto_fecha = {
            'id' : id['id'],
            'fecha_movimiento' : str(nueva_fecha_tipada)
        }
        creacion_json(self.variables.help_directory,self.variables.movement_date_document_file,id).actualizar_datos(nuevo_objeto_fecha)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Home_DateMovement()
    ventana.show()
    sys.exit(app.exec_())
