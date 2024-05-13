import sys
from Reports_Logic.globalModulesShare.resources import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import os
from ..ventanaspy.ventana_rutas import *
from .documentos_json import creacion_json
from .ContenedorVariables import Variables
from .mensajes_alertas import Mensajes_Alertas
from .Inicio_FechaMovimiento import *


class rutas(QMainWindow):
    def __init__(self):
        super(rutas, self).__init__()

        self.variables = Variables()
        self.ruta = self.variables.help_directory
        self.namejson = self.variables.documentSavingPaths
        self.json = creacion_json(self.ruta, self.namejson)

        self.ui = Ui_ventana_configuracion_rutasdocumentos()
        self.ui.setupUi(self)
        self.setWindowTitle("Registro de rutas")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.labelId.setVisible(False)

        self.ui.btn_btn_aceptar.clicked.connect(self.comprobar)

        self.ui.tabla_rutas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.tabla_rutas.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Custom
        )
        self.ui.tabla_rutas.setColumnWidth(0, 150)
        self.ui.tabla_rutas.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

        # self.actualizar_tabla()
        self.ui.tabla_rutas.itemClicked.connect(self.clic_celda)

        self.eliminar = self.ui.rb_rb_eliminar
        self.ingresar = self.ui.rb_rb_ingresar

        
        self.actualizar_tabla()


    def aceptarCallback(self):
        pass

    def comprobar(self):
        if self.eliminar.isChecked():
            self.eliminar_datos()
        elif self.ingresar.isChecked():
            self.ingresar_datos()
        else:
            pass

    def ingresar_datos(self):
        nombre = self.ui.txt_nombre.text().strip()
        ruta = self.ui.txt_ruta.text().strip()
        extension = self.ui.txt_extension_documento.text()
        objectNew = {
            "nombre" : "".join([nombre,extension]),
            "path" : ruta
        }
        if not (nombre and ruta):
            Mensajes_Alertas(
                "Datos incompletos",
                "Cuándo intentes almacenar algun elemento debes de tener en cuenta que es obligatorio ingresar ambos datos",
                QMessageBox.Icon.Warning,
                None,
                botones = [
                    ("Entendido" , self.aceptarCallback)
                ]
            )
        else:
            creacion_json(self.ruta, self.namejson, objectNew).agregar_json
            self.actualizar_tabla()
        self.ui.txt_nombre.clear()
        self.ui.txt_ruta.clear()
        

    def clic_celda(self, item):
        fila = item.row()
        columna = item.column()
        
        # Obtener el nombre y la ruta de la fila seleccionada
        nombre = self.ui.tabla_rutas.item(fila, 0).text()  # Columna 0 para el nombre
        ruta = self.ui.tabla_rutas.item(fila, 1).text()   # Columna 1 para la ruta
        
        # Buscar el ID correspondiente al nombre y la ruta
        id_objeto = None
        for objeto in self.json.comprobar_existencia:
            if objeto["nombre"] == nombre and objeto["path"] == ruta:
                id_objeto = objeto["id"]
                break

        # Verificar si se encontró el ID
        if id_objeto is not None:
            self.ui.labelId.setText(id_objeto)
        else:
            Mensajes_Alertas(
                "Dato no encontrado",
                "Cada elemento cuenta con un identificador y el que acabas de seleccionar no cuenta con ninguno, favor de volverlo a ingresar o eliminar",
                QMessageBox.Icon.Critical,
                None,
                botones = [
                    ("Entendido" , self.aceptarCallback)
                ]
            )
        
        # Actualizar los campos de texto con el nombre y la ruta
        self.ui.txt_nombre.setText(nombre.split(".")[0])
        self.ui.txt_ruta.setText(ruta)

    def actualizar_tabla(self):
        self.datos_json = self.json.comprobar_existencia
        self.ui.tabla_rutas.clearContents()
        self.ui.tabla_rutas.setRowCount(0)
        try:
            for row, item in enumerate(self.datos_json):
                self.ui.tabla_rutas.insertRow(row)
                for col, key in enumerate(["nombre", "path"]):
                    self.ui.tabla_rutas.setItem(row, col, QTableWidgetItem(str(item[key])))

            for fila in range(self.ui.tabla_rutas.rowCount()):
                for columna in range(self.ui.tabla_rutas.columnCount()):
                    celda = self.ui.tabla_rutas.item(fila, columna)
                    if celda:
                        celda.setFlags(celda.flags() & ~Qt.ItemFlag.ItemIsEditable)
        except:
            pass

    def eliminar_datos(self):
        keyId = {"id" : self.ui.labelId.text()}
        creacion_json(self.ruta, self.namejson, keyId).eliminar_datos_json
        self.actualizar_tabla()
        self.ui.txt_nombre.clear()
        self.ui.txt_ruta.clear()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = rutas()
    window.show()
    sys.exit(app.exec_())
