import sys
from resources import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import os
from .Rio_Bravo.UI.ventana_rutas import *
from .Rio_Bravo.Documento_ligas import *
from .Inicio_FechaMovimiento import *


class rutas(QMainWindow):
    def __init__(self):
        super(rutas, self).__init__()
        self.ui = Ui_ventana_configuracion_rutasdocumentos()
        self.ui.setupUi(self)
        self.setWindowTitle("Registro de rutas")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btn_btn_aceptar.clicked.connect(self.comprobar)
        self.ui.tabla_rutas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tabla_rutas.horizontalHeader().setSectionResizeMode(
            0, self.ui.tabla_rutas.horizontalHeader().Custom
        )
        self.ui.tabla_rutas.setColumnWidth(0, 150)
        self.ui.tabla_rutas.horizontalHeader().setSectionResizeMode(
            1, self.ui.tabla_rutas.horizontalHeader().Stretch
        )

        # self.actualizar_tabla()
        self.ui.tabla_rutas.itemClicked.connect(self.clic_celda)

        self.eliminar = self.ui.rb_rb_eliminar
        self.ingresar = self.ui.rb_rb_ingresar

        self.actualizar_tabla()


    def comprobar(self):
        if self.eliminar.isChecked():
            self.eliminar_datos()
        elif self.ingresar.isChecked():
            self.ingresar_datos()
        else:
            pass

    def clic_celda(self, item):
        fila = item.row()
        columna = item.column()
        if columna == 1:
            nombre = self.ui.tabla_rutas.item(fila, columna - 1).text()
            ruta = self.ui.tabla_rutas.item(fila, columna).text()
        elif columna == 0:
            nombre = self.ui.tabla_rutas.item(fila, columna).text()
            ruta = self.ui.tabla_rutas.item(fila, columna + 1).text()
        else:
            print("Error en la selección")
        self.ui.txt_nombre.setText(nombre.split(".")[0])
        self.ui.txt_ruta.setText(ruta)

    def actualizar_tabla(self):
        self.datos_json = CreacionJson().comprobar_existencia
        self.ui.tabla_rutas.clearContents()
        self.ui.tabla_rutas.setRowCount(0)

        for row, item in enumerate(self.datos_json):
            self.ui.tabla_rutas.insertRow(row)
            for col, key in enumerate(["Nombre_documento", "Ruta_destino_documento"]):
                self.ui.tabla_rutas.setItem(row, col, QTableWidgetItem(str(item[key])))

        for fila in range(self.ui.tabla_rutas.rowCount()):
            for columna in range(self.ui.tabla_rutas.columnCount()):
                celda = self.ui.tabla_rutas.item(fila, columna)
                if celda:
                    celda.setFlags(celda.flags() & ~Qt.ItemIsEditable)

    def ingresar_datos(self):
        nombre = self.ui.txt_nombre.text().strip()
        ruta = self.ui.txt_ruta.text().strip()
        extension = self.ui.txt_extension_documento.text()
        if not (nombre and ruta):
            print("Ambos están vacíos")
        else:
            CreacionJson(nombre, ruta, extension).Agregar_ruta
            self.actualizar_tabla()
            print("Al menos uno de ellos tiene contenido")
        self.ui.txt_nombre.clear()
        self.ui.txt_ruta.clear()

    def eliminar_datos(self):
        nombre = self.ui.txt_nombre.text() + self.ui.txt_extension_documento.text()
        ruta = self.ui.txt_ruta.text()
        CreacionJson().Eliminar_ruta(nombre, ruta)
        self.actualizar_tabla()
        self.ui.txt_nombre.clear()
        self.ui.txt_ruta.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = rutas()
    window.show()
    sys.exit(app.exec_())
