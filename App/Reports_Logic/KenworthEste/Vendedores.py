#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.resources import *
from ..globalModulesShare.ContenedorVariables import *
from ..ventanaspy.IU_VENDEDORES import *
from ..globalModulesShare.documentos_json import*
from ..globalModulesShare.mensajes_alertas import *

class Vendedores(QWidget, Variables, ):
    def __init__(self):
        super(Vendedores,self).__init__()

#COMMENT: METTODOS POR PESTAÑA
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
#{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}
#COMMENT: CREAR LA VENTANA
        self.ui = Ui_Formulario_Vendedores()
        self.ui.setupUi(self)
        self.ui.Vendedores_Refacciones.setCurrentIndex(0)
        self.setWindowTitle("Clasificación de Vendedores")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.tabla_vendedoresrefacciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #COMMENTLINE: AMPLIAMOS LAS COLUMNAS AL ESPACIO DEL CONTENEDOR DE LA TABLA.
        self.ui.tabla_vendedoresrefacciones_servicio.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #COMMENTLINE: AMPLIAMOS LAS COLUMNAS AL ESPACIO DEL CONTENEDOR DE LA TABLA.
        self.ui.btn_aceptar_vendedores.clicked.connect(self.comprobar_evento) #COMMENTLINE: CONECTAMOS LA FUNCION AL BOTON DE ACTUALIZAR.
        self.ui.rb_agregar.toggled.connect(self.id_blanco) #COMMENTLINE: CONECTAMOS EL RADIOBUTTOM AL METODO PARA PONER EN BLANCO EL CAMPO DE ID.
        self.ui.rb_agregar_servicio.toggled.connect(self.id_blanco) #COMMENTLINE: CONECTAMOS EL RADIOBUTTOM AL METODO PARA PONER EN BLANCO EL CAMPO DE ID.
        self.ui.ledit_idrefacciones.setEnabled(False) #COMMENTLINE: INHABILITAMOS EL CAMPO DE ID_REFACCIONES.
        self.ui.ledit_idservicio.setEnabled(False) #COMMENTLINE: INHABILITAMOS EL CAMPOR DE ID_SERVICIO.
        self.ui.tabla_vendedoresrefacciones.itemClicked.connect(self.clic_celda_refacciones) #COMMENTLINE: CONECTAMOS EL EVENTO DE CLIC A LA TABLA DE REFACCIONES.
        self.ui.tabla_vendedoresrefacciones_servicio.itemClicked.connect(self.clic_celda_servicio)
        self.ui.Vendedores_Refacciones.currentChanged.connect(self.Actualizar_tablas)
        self.Actualizar_tablas()
#{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}

#COMMENT: COLOCAR EN BLANCO EL CAMPO DE ID CUANDO SE SELECCIONE AGREGAR.
    def id_blanco(self):
        if self.ui.rb_agregar.isChecked():
            self.ui.ledit_idrefacciones.clear()
        elif self.ui.rb_agregar_servicio.isChecked():
            self.ui.ledit_idservicio.clear()
#{{{{{{{{{}}}}}}}}}

#COMMENT: OBTENER LOS DATOS AL DAR CLIC EN LA TABLA DE SERVICIO
    def clic_celda_servicio(self, item):
        if (self.ui.rb_agregar_servicio.isChecked()):
            return
        fila = item.row()
        columna = item.column()
        if columna == 0:
            id = self.ui.tabla_vendedoresrefacciones_servicio.item(fila, columna - 0).text()
        else:
            print("Error en la selección")
            pass
        try:
            self.ui.ledit_idservicio.setText(id)
            id_objeto = {"id" : id}
            elementos = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio,id_objeto).obtener_datos_json_por_id
            self.ui.ledit_nombrevendedor_servicio.setText(elementos["Vendedor"])
            self.ui.ledit_depaventa_servicio.setText(elementos["Depa_Venta"])
            self.ui.ledit_depa_servicio.setText(elementos["Depa"])
        except:
            pass
#{{{{{{{{{{{}}}}}}}}}}}

#COMMENT: OBTENER LOS DATOS AL DAR CLIC EN LA TABLA DE REFACCIONES
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
#{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}
  
#COMMENT: METODO PARA ACTUALIZAR LAS TABLAS
    def Actualizar_tablas(self, index = 0):
        if (self.obtener_tab_activo() == 0):
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
        elif (self.obtener_tab_activo() == 1):
            self.datos_json = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio).comprobar_existencia
            self.ui.tabla_vendedoresrefacciones_servicio.clearContents()
            self.ui.tabla_vendedoresrefacciones_servicio.setRowCount(0)

            for row, item in enumerate(self.datos_json):
                self.ui.tabla_vendedoresrefacciones_servicio.insertRow(row)
                for col, key in enumerate(["id","Vendedor","Depa_Venta","Depa"]):
                    self.ui.tabla_vendedoresrefacciones_servicio.setItem(row, col, QTableWidgetItem(str(item[key])))

            for fila in range(self.ui.tabla_vendedoresrefacciones_servicio.rowCount()):
                for columna in range(self.ui.tabla_vendedoresrefacciones_servicio.columnCount()):
                    celda = self.ui.tabla_vendedoresrefacciones_servicio.item(fila, columna)
                    if celda:
                        celda.setFlags(celda.flags() & ~Qt.ItemIsEditable)
#{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}

#COMMENT: OBTENEMOS EL INDICE DE LA PESTAÑA
    def obtener_tab_activo(self):
        ventana_activa = self.ui.Vendedores_Refacciones.currentIndex()
        return ventana_activa
#{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}

#COMMENT:COMPROBAMOS EL EVENTO AL PRESIONAR EL BOTON DE ACTUALIZAR
    def comprobar_evento(self):
        tipo_ventana = self.obtener_tab_activo()
        if tipo_ventana in self.acciones_por_pestañas:
#COMMENT:VERIFICA QUE ACCION ESTA SELECCIONADA EN LA PESTAÑA ACTIVA
            for accion, funcion in self.acciones_por_pestañas[tipo_ventana].items():
                if getattr(self.ui, f"rb_{accion}").isChecked() and accion == "agregar": #COMMENTLINE: METODO PARA AGREGAR REFACCIONES
                    nombre = self.ui.ledit_nombrevendedor.text()
                    sucursal = self.ui.ledit_sucursal.text()
                    departamento_venta = self.ui.ledit_depaventa.text()
                    departamento = self.ui.ledit_depa.text()
                    cargo = self.ui.ledit_cargo.text()
                    if (nombre and sucursal and departamento_venta and departamento and cargo):
                        funcion(nombre, sucursal,departamento_venta,departamento,cargo)
                    else:
                        Mensajes_Alertas(
                            "Datos Incompletos.",
                            "Para completar la operación, deberá de ingresar obligatoriamente todos los campos.",
                            QMessageBox.Warning,  # Aquí se pasa el tipo de ícono
                            "Algunos reportes necesitan de algunos apartados en especifico, es por ello que es necesario que se llenen todos los campos ",
                            botones = [
                                ("Aceptar", self.aceptar_callback)
                            ]
                        ).mostrar
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui,f'rb_{accion}').isChecked() and accion == "eliminar": #COMMENTLINE: METODO PARA ELIMINAR REFACCIONES
                    indice = self.ui.ledit_idrefacciones.text()
                    funcion(indice)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui, f'rb_{accion}').isChecked() and accion == "actualizar": #COMMENTLINE: METODO PARA ACTUALIZAR REFACCIONES
                    indice = self.ui.ledit_idrefacciones.text()
                    nombre = self.ui.ledit_nombrevendedor.text()
                    sucursal = self.ui.ledit_sucursal.text()
                    departamento_venta = self.ui.ledit_depaventa.text()
                    departamento = self.ui.ledit_depa.text()
                    cargo = self.ui.ledit_cargo.text()
                    funcion(indice, nombre, sucursal,departamento_venta,departamento,cargo)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                if getattr(self.ui, f"rb_{accion}").isChecked() and accion == "agregar_servicio": #COMMENTLINE: METODO PARA AGREGAR SERVICIO
                    nombre = self.ui.ledit_nombrevendedor_servicio.text()
                    departamento_venta = self.ui.ledit_depaventa_servicio.text()
                    departamento = self.ui.ledit_depa_servicio.text()
                    if (nombre and departamento_venta and departamento):
                        funcion(nombre,departamento_venta,departamento)
                    else:
                        Mensajes_Alertas(
                            "Datos Incompletos.",
                            "Para completar la operación, deberá de ingresar obligatoriamente todos los campos.",
                            QMessageBox.Warning,  # Aquí se pasa el tipo de ícono
                            "Algunos reportes necesitan de algunos apartados en especifico, es por ello que es necesario que se llenen todos los campos ",
                            botones = [
                                ("Aceptar", self.aceptar_callback)
                            ]
                        ).mostrar
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui,f'rb_{accion}').isChecked() and accion == "eliminar_servicio": #COMMENTLINE: METODO PARA ELIMINAR SERVICIO
                    indice = self.ui.ledit_idservicio.text()
                    funcion(indice)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
                elif getattr(self.ui, f'rb_{accion}').isChecked() and accion == "actualizar_servicio": #COMMENTLINE: METODO PARA ACTUALIZAR SERVICIO
                    indice = self.ui.ledit_idservicio.text()
                    nombre = self.ui.ledit_nombrevendedor_servicio.text()
                    departamento_venta = self.ui.ledit_depaventa_servicio.text()
                    departamento = self.ui.ledit_depa_servicio.text()
                    funcion(indice, nombre,departamento_venta,departamento)
                    self.lineas_en_blanco()
                    self.Actualizar_tablas()
#{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}                    

#COMMENT: PONEMOS LOS CAMPOS DE TEXTO EN BLANCO                    
    def lineas_en_blanco(self):
        if(self.obtener_tab_activo()==0):
            self.ui.ledit_idrefacciones.clear()
            self.ui.ledit_nombrevendedor.clear()
            self.ui.ledit_sucursal.clear()
            self.ui.ledit_depaventa.clear()
            self.ui.ledit_depa.clear()
            self.ui.ledit_cargo.clear()
        elif(self.obtener_tab_activo()==1):
            self.ui.ledit_idservicio.clear()
            self.ui.ledit_nombrevendedor_servicio.clear()
            self.ui.ledit_depaventa_servicio.clear()
            self.ui.ledit_depa_servicio.clear()

    def aceptar_callback(self):
        pass
#{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}

#COMMENT:CLASE PARA LA LOGICA DE LA PESTAÑA DE REFACCIONES
class funciones_vendedores_refacciones(Variables):
    def __init__(self):
        self.direccion_documento = os.path.join(Variables().ruta_deapoyo,Variables().nombre_documento_clasificacion_vendedores_refacciones)
        

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
    def __init__(self):
        self.direccion_documento = os.path.join(Variables().ruta_deapoyo,Variables().nombre_documento_clasificacion_vendedores_servicio)
        #COMMENT: COMPROBAR LA EXISTENCIA DE LOS DOCUMENTOS        
        
    def actualizar_vendedores_servicio(self,indice, nombre, sucursal,departamento_venta,departamento,cargo):
        id = {"id" : indice}
        datos_anteriores = creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio,id).obtener_datos_json_por_id
        if datos_anteriores:
            datos_nuevos = {
                "id" : id["id"],
                "Vendedor": nombre,
                "Depa_Venta": departamento_venta,
                "Depa": departamento
            }
            creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio,id).actualizar_datos(datos_nuevos)
    def agregar_vendedores_servicio(self,nombre = None,depaventa=None,depa=None):
        objeto = {
            "Vendedor" : nombre,
            "Depa_Venta" : depaventa,
            "Depa" : depa
        }
        creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio, objeto).agregar_json
    def eliminar_vendedores_servicio(self, indice):
        elemento_eliminar = {"id" : indice}
        creacion_json(Variables().ruta_deapoyo, Variables().nombre_documento_clasificacion_vendedores_servicio,elemento_eliminar).eliminar_datos_json



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Vendedores()
    window.show()
    sys.exit(app.exec_())