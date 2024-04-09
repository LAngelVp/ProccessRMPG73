#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from resources import *
from .Logica_Reportes.Variables.ContenedorVariables import *
from .UI.IU_VENDEDORES import *
from ..documentos_json import*
from ..mensajes_alertas import *

class Vendedores(QWidget, Variables, ):
    def __init__(self):
        super(Vendedores,self).__init__()

        self.acciones_por_pestañas = {
            0: {
                "actualizar": funciones_vendedores_refacciones().actualizar_vendedores_refacciones, 
                "agregar": funciones_vendedores_refacciones().agregar_vendedores_refacciones, 
                "eliminar": funciones_vendedores_refacciones().eliminar_vendedores_refacciones
                },
            1: {
                "actualizar_servicio": funciones_vendedores_servicio().actualizar_vendedores_servicio, 
                "agregar_servicio": funciones_vendedores_servicio().agregar_vendedores_servicio, 
                "eliminar_servicio": funciones_vendedores_servicio().eliminar_vendedores_servicio
                }
        }

#COMMENT: CREAR LA VENTANA    
        self.ui = Ui_Formulario_Vendedores()
        self.ui.setupUi(self)
        self.ui.Vendedores_Refacciones.setCurrentIndex(0)
        self.setWindowTitle("Clasificación de Vendedores")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.tabla_vendedoresrefacciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #COMMENTLINE: AMPLIAMOS LAS COLUMNAS AL ESPACIO DEL CONTENEDOR DE LA TABLA.
        self.ui.tabla_vendedoresrefacciones_servicio.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.btn_aceptar_vendedores.clicked.connect(self.comprobar_evento)



        self.ui.rb_agregar.toggled.connect(self.id_blanco)

        self.Actualizar_tablas()

        self.ui.ledit_idrefacciones.setEnabled(False)

        self.ui.tabla_vendedoresrefacciones.itemClicked.connect(self.clic_celda_refacciones)


    def id_blanco(self):
        if self.ui.rb_agregar.isChecked():
            self.ui.ledit_idrefacciones.clear()


    def clic_celda_refacciones(self, item):
        if (self.ui.rb_agregar.isChecked()):
            return
        fila = item.row()
        columna = item.column()
        if columna == 0:
            id = self.ui.tabla_vendedoresrefacciones.item(fila, columna - 0).text()
        else:
            print("Error en la selección")
            pass
        try:
            self.ui.ledit_idrefacciones.setText(id)
            id_objeto = {"id" : id}
            elementos = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones,id_objeto).obtener_datos_json_por_id
            self.ui.ledit_nombrevendedor.setText(elementos["vendedor"])
            self.ui.ledit_sucursal.setText(elementos["sucursal"])
            self.ui.ledit_cargo.setText(elementos["jerarquia"])
            self.ui.ledit_depaventa.setText(elementos["depto venta"])
            self.ui.ledit_depa.setText(elementos["departamento"])
        except:
            pass

    def Actualizar_tablas(self):
        self.datos_json = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones).comprobar_existencia
        self.ui.tabla_vendedoresrefacciones.clearContents()
        self.ui.tabla_vendedoresrefacciones.setRowCount(0)

        for row, item in enumerate(self.datos_json):
            self.ui.tabla_vendedoresrefacciones.insertRow(row)
            for col, key in enumerate(["id","vendedor", "sucursal","depto venta","departamento","jerarquia"]):
                self.ui.tabla_vendedoresrefacciones.setItem(row, col, QTableWidgetItem(str(item[key])))

        for fila in range(self.ui.tabla_vendedoresrefacciones.rowCount()):
            for columna in range(self.ui.tabla_vendedoresrefacciones.columnCount()):
                celda = self.ui.tabla_vendedoresrefacciones.item(fila, columna)
                if celda:
                    celda.setFlags(celda.flags() & ~Qt.ItemIsEditable)


    def obtener_tab_activo(self):
        ventana_activa = self.ui.Vendedores_Refacciones.currentIndex()
        return ventana_activa
    
    def comprobar_evento(self):
        tipo_ventana = self.obtener_tab_activo()
        if tipo_ventana in self.acciones_por_pestañas:
            eliminar_seleccionado = getattr(self.ui, "rb_eliminar").isChecked()
            actualizar_seleccionado = getattr(self.ui, "rb_actualizar").isChecked()
        # Verificar qué acción está seleccionada en la pestaña activa
            for accion, funcion in self.acciones_por_pestañas[tipo_ventana].items():
                if getattr(self.ui, f"rb_{accion}").isChecked() and not eliminar_seleccionado and not actualizar_seleccionado:
                    nombre = self.ui.ledit_nombrevendedor.text()
                    sucursal = self.ui.ledit_sucursal.text()
                    departamento_venta = self.ui.ledit_depaventa.text()
                    departamento = self.ui.ledit_depa.text()
                    cargo = self.ui.ledit_cargo.text()
                    if (nombre and sucursal and departamento_venta and departamento and cargo):
                        funcion(nombre, sucursal,departamento_venta,departamento,cargo)
                    else:
                        Mensajes_Alertas.mostrar(
                            "Datos Incompletos.",
                            "Para completar la operación, deberá de ingresar obligatoriamente todos los campos.",
                            QMessageBox.Warning,  # Aquí se pasa el tipo de ícono
                            [("Aceptar", QMessageBox.AcceptRole)]
                        )
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui,f'rb_{accion}').isChecked() and accion == "eliminar":
                    indice = self.ui.ledit_idrefacciones.text()
                    funcion(indice)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui, f'rb_{accion}').isChecked() and accion == "actualizar":
                    indice = self.ui.ledit_idrefacciones.text()
                    nombre = self.ui.ledit_nombrevendedor.text()
                    sucursal = self.ui.ledit_sucursal.text()
                    departamento_venta = self.ui.ledit_depaventa.text()
                    departamento = self.ui.ledit_depa.text()
                    cargo = self.ui.ledit_cargo.text()
                    funcion(indice, nombre, sucursal,departamento_venta,departamento,cargo)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui, f"rb_{accion}").isChecked():
                    funcion()
    def lineas_en_blanco(self):
        self.ui.ledit_idrefacciones.clear()
        self.ui.ledit_nombrevendedor.clear()
        self.ui.ledit_sucursal.clear()
        self.ui.ledit_depaventa.clear()
        self.ui.ledit_depa.clear()
        self.ui.ledit_cargo.clear()

class funciones_vendedores_refacciones(Variables):
    def __init__(self):
        self.direccion_documento = os.path.join(Variables().ruta_deapoyo,Variables().nombre_documento_clasificacion_vendedores_refacciones)
        
        #COMMENT: COMPROBAR LA EXISTENCIA DE LOS DOCUMENTOS        
        try:
            pass
            # self.json_vendedores_refacciones = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones).comprobar_existencia
        except FileNotFoundError as error:
            pass

    def actualizar_vendedores_refacciones(self,indice, nombre, sucursal,departamento_venta,departamento,cargo):
        id = {"id" : indice}
        datos_anteriores = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones,id).obtener_datos_json_por_id
        if datos_anteriores:
            datos_nuevos = {
                "id" : id["id"],
                "vendedor": nombre,
                "sucursal": sucursal,
                "depto venta": departamento_venta,
                "departamento": departamento,
                "jerarquia": cargo
            }
            creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones,id).actualizar_datos(datos_nuevos)

    def agregar_vendedores_refacciones(self,nombre = None,sucursal=None,depaventa=None,depa=None,cargo=None):
        objeto = {
            "vendedor" : nombre,
            "sucursal" : sucursal,
            "depto venta" : depaventa,
            "departamento" : depa,
            "jerarquia" : cargo
        }
        creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones, objeto).agregar_json
        
    
    def eliminar_vendedores_refacciones(self, indice):
        elemento_eliminar = {"id" : indice}
        creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_refacciones,elemento_eliminar).eliminar_datos_json


class funciones_vendedores_servicio(Variables):
    def __init__(self, nombre = None, departamento_venta = None, departamento = None):
        self.nombre = nombre
        self.departamento_venta = departamento_venta
        self.departamento = departamento

        #COMMENT: COMPROBAR LA EXISTENCIA DE LOS DOCUMENTOS        
        try:
            self.json_vendedores_servicio = Variables().vendedores_y_depas_este_servicio()
        except FileNotFoundError as error:
            pass

    def actualizar_vendedores_servicio(self):
        print (4)
    def agregar_vendedores_servicio(self):
        print (5)
    def eliminar_vendedores_servicio(self):
        print (6)



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Vendedores()
    window.show()
    sys.exit(app.exec_())