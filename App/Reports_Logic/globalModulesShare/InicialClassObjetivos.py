#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon
from .resources import *
from ..ventanaspy.V_AgregarObjetivos import *
from PyQt6.QtWidgets import *
from PyQt6 import *
from .ContenedorVariables import Variables
from .documentos_json import creacion_json
from .mensajes_alertas import Mensajes_Alertas

class ClassPrincipalObjPagos(QMainWindow):
    def __init__(self):
        super(ClassPrincipalObjPagos, self).__init__()
        self.variables = Variables()

        self.ruta = self.variables.help_directory
        self.nameJson = self.variables.customerPaymentGoals
        self.claseJson = creacion_json(self.ruta, self.nameJson).comprobar_existencia

        Icon_aceptar = QIcon(":/Source/comprobado.png")
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        self.UI.btn_Aceptar.setIcon(Icon_aceptar)
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.UI.btn_Aceptar.clicked.connect(self.ComprobarCheck)
        self.UI.CB_Sucursales.activated.connect(self.seleccionarSucursal)
        self.UI.labelId.setVisible(False)
        
        self.mostrar_Sucursales()


    def limpiarCampos(self):
        self.UI.labelId.clear()
        self.UI.LE_Sucursal.clear()
        self.UI.LE_Objetivo.clear()


    def aceptarCallback(self):
        pass

# // Mostrar las sucursales en el ComboBox

    def mostrar_Sucursales(self):
        self.UI.CB_Sucursales.clear()
        numDatos = len(creacion_json(self.ruta, self.nameJson).comprobar_existencia)
        if numDatos == 0:
                self.UI.CB_Sucursales.addItem("Sin Sucursales")
        for obj in creacion_json(self.ruta, self.nameJson).comprobar_existencia:
            nom_sucursal = obj["nombre"]
            self.UI.CB_Sucursales.addItem(nom_sucursal)

#-------------------------------------------
# COMPROBAMOS QUE ESTE SELECCIONADO UN RADIO BOTON PARA REALIZAR LAS ACCIONES
    def ComprobarCheck(self):
        if self.UI.RB_Agregar.isChecked():
            self.AgregarObjeto()
        elif self.UI.RB_Modificar.isChecked():
            self.modificar_objetivos()
        elif self.UI.RB_Eliminar.isChecked():
            self.EliminarObjeto()
        else:
            Mensajes_Alertas(
                "Opciones de selección",
                "Ninguna de las opciones disponibles para manipular el archivo estan seleccionadas",
                QMessageBox.Icon.Information,
                None,
                botones=[
                    ("Entendido", self.aceptarCallback)
                ]
            )
        self.mostrar_Sucursales()
    
#--------------------------------------------
# AGREGAR
    def AgregarObjeto(self):
        sucursal = self.UI.LE_Sucursal.text().strip()
        objetivo = self.UI.LE_Objetivo.text().strip()
        if (objetivo.isnumeric()):
            objectContain = {
                'nombre' : sucursal,
                'objetivo' : objetivo
            }
            creacion_json(self.ruta, self.nameJson, objectContain).agregar_json
        else:
            Mensajes_Alertas(
                'Intento al agregar objetivo',
                'Estas ingresando una cadena de caracteres en el campo de objetivo, dicho campo solo permite números',
                QMessageBox.Icon.Warning,
                None,
                botones = [
                    ('Entendido', self.aceptarCallback)
                ]
            )
        self.limpiarCampos()
        self.mostrar_Sucursales()

#-------------------------------------------
# MODIFICAR SUCURSALES

    def modificar_objetivos(self):
        keyId = {
            "id" : self.UI.labelId.text()
        }
        new_sucursal = self.UI.LE_Sucursal.text().strip()
        new_obj = self.UI.LE_Objetivo.text().strip()
        self.jsonActual = creacion_json(self.ruta, self.nameJson, keyId).obtener_datos_json_por_id
        if (new_obj.isnumeric()):
            if self.jsonActual:
                datos_nuevos = {
                    "id" : keyId["id"],
                    "nombre" : new_sucursal,
                    "objetivo" : new_obj,
                }
                creacion_json(self.ruta, self.nameJson, keyId).actualizar_datos(datos_nuevos)
        else:
            Mensajes_Alertas(
                'Intento al agregar objetivo',
                'Estas ingresando una cadena de caracteres en el campo de objetivo, dicho campo solo permite números',
                QMessageBox.Icon.Warning,
                None,
                botones = [
                    ('Entendido', self.aceptarCallback)
                ]
            )
        self.limpiarCampos()
        self.mostrar_Sucursales()
    
        
# ELIMINAR

    def EliminarObjeto(self):
        idElementDelete = {"id" : self.UI.labelId.text()}
        creacion_json(self.ruta, self.nameJson, idElementDelete).eliminar_datos_json
        self.limpiarCampos()
        self.mostrar_Sucursales()


# SELECCION DE ELEMENTOS

    def seleccionarSucursal(self):
        elemento = self.UI.CB_Sucursales.currentText()
        for i in creacion_json(self.ruta, self.nameJson).comprobar_existencia:
            keyId = i["id"]
            nombre_s = i["nombre"]
            obj_s = i["objetivo"]
            if (nombre_s == elemento):
                self.UI.labelId.setText(keyId)
                self.UI.LE_Sucursal.setText(nombre_s)
                self.UI.LE_Objetivo.setText(obj_s)




if __name__ == '__main__':
    app = QApplication (sys.argv)
    Ventana = ClassPrincipalObjPagos()
    Ventana.show()
    sys.exit(app.exec_())
