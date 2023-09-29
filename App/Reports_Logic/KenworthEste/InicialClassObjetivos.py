import sys
import os
import json
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from .UI.V_AgregarObjetivos import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from resources import *
from .Logica_Reportes.Variables.ContenedorVariables import Variables
 
class ClassPrincipalObjPagos(QMainWindow, Variables):
    def __init__(self):
        super(ClassPrincipalObjPagos, self).__init__()
        Icon_aceptar = QIcon(":/Source/comprobado.png")
        self.rutaJSON = Variables().ruta_deapoyo
        self.jsonObjetivos = "JsonObjetivos.json"
        self.rutaJsonCompleta = os.path.join(self.rutaJSON,self.jsonObjetivos)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        self.UI.btn_Aceptar.setIcon(Icon_aceptar)
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.comprobarSiExisteJsonPagos(self.rutaJsonCompleta)
        self.UI.btn_Aceptar.clicked.connect(self.ComprobarCheck)
        self.mostrar_Sucursales()
        self.UI.CB_Sucursales.activated.connect(self.seleccionarSucursal)
#_--------------------------------------------    
# COMPROBAMOS LA EXISTENCIA DEL DOCUMENTO.
    def comprobarSiExisteJsonPagos(self, ruta):
        if os.path.exists(ruta): # SI EXISTE
            pass
        else: 
            self.crearDocumento(ruta) # SI NO EXISTE
#---------------------------------------------
# CREAMOS EL DOCUMENTO.
    def crearDocumento(self, ruta):
        datos_nuevos = []
        with open(ruta, "w") as docu:
            json.dump(datos_nuevos, docu, indent=4)
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
            QMessageBox.information(self, "Advertencia", "Ningún botón de opción está marcado.")
#--------------------------------------------
# AGREGAR
    def AgregarObjeto(self):
        sucursal = self.UI.LE_Sucursal.text().strip()
        objetivo = self.UI.LE_Objetivo.text().strip()
        datos = self.abrirDocumento()
        if (objetivo.isnumeric()):
            self.escribirDocumento(datos, sucursal, objetivo)
        else:
            QMessageBox.information(self, "Advertencia", "El objetivo debe de ser numerico.")
        self.mostrar_Sucursales()
#--------------------------------------------
# MODIFICAR

    def mostrar_Sucursales(self):
        sucursal = self.abrirDocumento()
        self.UI.CB_Sucursales.clear()
        for obj in sucursal:
            nom_sucursal = obj["Sucursal"]
            self.UI.CB_Sucursales.addItem(nom_sucursal)
#-------------------------------------------
# MODIFICAR SUCURSALES

    def modificar_objetivos(self):
        new_sucursal = self.UI.LE_Sucursal.text().strip()
        new_obj = self.UI.LE_Objetivo.text().strip()
        json = self.abrirDocumento()
        if (new_obj.isnumeric()):
            for i in json:
                if (i["Sucursal"] == new_sucursal):
                    i["Objetivo"] = new_obj
                else:
                    continue
        else:
            QMessageBox.information(self, "Advertencia", "El objetivo debe de ser numerico.")
        self.guardarDocumento(json)
    
        
# ELIMINAR

    def EliminarObjeto(self):
        json = self.abrirDocumento()
        sucursal_a_eliminar = self.UI.LE_Sucursal.text()

        # Crear una nueva lista sin el objeto a eliminar
        json_data = [item for item in json if item["Sucursal"] != sucursal_a_eliminar]

        # Guardar los cambios en el archivo JSON
        self.guardarDocumento(json_data)
        self.mostrar_Sucursales()

# SELECCION DE ELEMENTOS

    def seleccionarSucursal(self):
        elemento = self.UI.CB_Sucursales.currentText()
        json = self.abrirDocumento()
        for i in json:
            nombre_s = i["Sucursal"]
            obj_s = i["Objetivo"]
            if (nombre_s == elemento):
                self.UI.LE_Sucursal.setText(nombre_s)
                self.UI.LE_Objetivo.setText(obj_s)
#-------------------------------------------
# FUNCIONES DE ABRIR Y ESCRIBIR EL DOCUMENTO
#_------------------------------------------
# LEER

    def abrirDocumento(self):
        with open(self.rutaJsonCompleta, "r") as documento:
            self.datos_existentes = json.load(documento)
        return self.datos_existentes
    
# ESCRIBIR
    def escribirDocumento(self, matriz, sucursal, objetivo):
        matriz.append({"Sucursal": sucursal, "Objetivo": objetivo})
        with open(self.rutaJsonCompleta, "w") as docu:
            json.dump(matriz, docu, indent=4)

    def guardarDocumento(self, json_data):
        with open(self.rutaJsonCompleta, 'w') as file:
            json.dump(json_data, file, indent=4)



if __name__ == '__main__':
    app = QApplication (sys.argv)
    Ventana = ClassPrincipalObjPagos()
    Ventana.show()
    sys.exit(app.exec_())
