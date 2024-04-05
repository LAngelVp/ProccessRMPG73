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
from .Logica_Reportes.Variables.ContenedorVariables import *
from .UI.IU_VENDEDORES import *
from ..documentos_json import*

class Vendedores(QWidget, Variables):
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

        


    def obtener_tab_activo(self):
        ventana_activa = self.ui.Vendedores_Refacciones.currentIndex()
        return ventana_activa
    
    def comprobar_evento(self):
        tipo_ventana = self.obtener_tab_activo()
        if tipo_ventana in self.acciones_por_pestañas:
        # Verificar qué acción está seleccionada en la pestaña activa
            for accion, funcion in self.acciones_por_pestañas[tipo_ventana].items():
                if getattr(self.ui, f"rb_{accion}").isChecked():
                    nombre = self.ui.ledit_nombrevendedor.text()
                    sucursal = self.ui.ledit_sucursal.text()
                    departamento_venta = self.ui.ledit_depaventa.text()
                    departamento = self.ui.ledit_depa.text()
                    cargo = self.ui.ledit_cargo.text()
                    funcion(nombre, sucursal,departamento_venta,departamento,cargo)
                elif getattr(self.ui, f"rb_{accion}").isChecked():
                    funcion()

class funciones_vendedores_refacciones(Variables):
    def __init__(self):
        self.ruta_json_vendedores_refacciones =  Variables().ruta_deapoyo
        self.nombre_documento = "Vendedores_refacciones_departamentos.json"
        #COMMENT: COMPROBAR LA EXISTENCIA DE LOS DOCUMENTOS        
        try:
            self.json_vendedores_refacciones = Variables().clasificacion_vendedores_departamentos_refacciones()
        except FileNotFoundError as error:
            pass

    def actualizar_vendedores_refacciones(self,nombre = None,sucursal=None,depaventa=None,depa=None,cargo=None):
        data_default = []
        creacion_json(self.ruta_json_vendedores_refacciones, self.nombre_documento,data_default).comprobar_existencia
    def agregar_vendedores_refacciones(self,nombre,sucursal,depaventa,depa,cargo):
        objeto = {
            "vendedor" : nombre,
            "sucursal" : sucursal,
            "depto venta" : depaventa,
            "departamento" : depa,
            "jerarquia" : cargo
        }
        print (objeto)
        creacion_json(self.ruta_json_vendedores_refacciones, self.nombre_documento, objeto).actualizar_json
    def eliminar_vendedores_refacciones(self):
        print (3)

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